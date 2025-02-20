unified_memory = True
import os, time, gc
if unified_memory:
  ENV = {"TF_FORCE_UNIFIED_MEMORY":"1", "XLA_PYTHON_CLIENT_MEM_FRACTION":"4.0"}
  for k,v in ENV.items(): os.environ[k] = v
if not os.path.isdir("params"):
  # get code
  print("installing ColabDesign")
  os.system("(mkdir params; apt-get install aria2 -qq; \
  aria2c -q -x 16 https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar; \
  tar -xf alphafold_params_2022-12-06.tar -C params; touch params/done.txt )&")

  os.system("pip -q install git+https://github.com/sokrypton/ColabDesign.git@gamma")
  os.system("ln -s /usr/local/lib/python3.*/dist-packages/colabdesign colabdesign")
  os.system("wget https://raw.githubusercontent.com/sokrypton/ColabFold/main/colabfold/colabfold.py -O colabfold_utils.py")

  # install hhsuite
  print("installing HHsuite")
  os.makedirs("hhsuite", exist_ok=True)
  os.system(f"curl -fsSL https://github.com/soedinglab/hh-suite/releases/download/v3.3.0/hhsuite-3.3.0-SSE2-Linux.tar.gz | tar xz -C hhsuite/")

  print("installing AnAnaS")
  os.system("wget -qnc https://files.ipd.uw.edu/krypton/ananas")
  os.system("wget -qnc https://files.ipd.uw.edu/krypton/make_symmdef_file.pl")
  os.system("chmod +x ananas")

  # download params
  if not os.path.isfile("params/done.txt"):
    print("downloading AlphaFold params")
    while not os.path.isfile("params/done.txt"):
      time.sleep(5)
if "hhsuite" not in os.environ['PATH']:
  os.environ['PATH'] += ":hhsuite/bin:hhsuite/scripts"

import re, tempfile
from IPython.display import HTML
from google.colab import files
import numpy as np
from colabdesign import mk_af_model, clear_mem
from colabdesign.af.contrib import predict
from colabdesign.af.contrib.cyclic import add_cyclic_offset
from colabdesign.shared.protein import _np_rmsd, _np_kabsch
from colabdesign.shared.plot import plot_pseudo_3D, pymol_cmap

import jax
import jax.numpy as jnp
from colabfold_utils import run_mmseqs2
import matplotlib.pyplot as plt
import string
import numpy as np

def clear_mem():
  backend = jax.lib.xla_bridge.get_backend()
  for buf in backend.live_buffers(): buf.delete()

def get_pdb(pdb_code=""):
  if pdb_code is None or pdb_code == "":
    upload_dict = files.upload()
    pdb_string = upload_dict[list(upload_dict.keys())[0]]
    with open("tmp.pdb","wb") as out: out.write(pdb_string)
    return "tmp.pdb"
  elif os.path.isfile(pdb_code):
    return pdb_code
  elif len(pdb_code) == 4:
    os.makedirs("tmp",exist_ok=True)
    os.system(f"wget -qnc https://files.rcsb.org/download/{pdb_code}.cif -P tmp/")
    return f"tmp/{pdb_code}.cif"
  else:
    os.makedirs("tmp",exist_ok=True)
    os.system(f"wget -qnc https://alphafold.ebi.ac.uk/files/AF-{pdb_code}-F1-model_v4.pdb -P tmp/")
    return f"tmp/AF-{pdb_code}-F1-model_v4.pdb"

def run_hhalign(query_sequence, target_sequence, query_a3m=None, target_a3m=None):
  with tempfile.NamedTemporaryFile() as tmp_query, \
  tempfile.NamedTemporaryFile() as tmp_target, \
  tempfile.NamedTemporaryFile() as tmp_alignment:
    if query_a3m is None:
      tmp_query.write(f">Q\n{query_sequence}\n".encode())
      tmp_query.flush()
      query_a3m = tmp_query.name
    if target_a3m is None:
      tmp_target.write(f">T\n{target_sequence}\n".encode())
      tmp_target.flush()
      target_a3m = tmp_target.name
    os.system(f"hhalign -hide_cons -i {query_a3m} -t {target_a3m} -o {tmp_alignment.name}")
    X, start_indices = predict.parse_hhalign_output(tmp_alignment.name)
  return X, start_indices

def run_do_not_align(query_sequence, target_sequence, **arg):
  return [query_sequence,target_sequence],[0,0]

def run_hhfilter(input, output, id=90, qid=10):
  os.system(f"hhfilter -id {id} -qid {qid} -i {input} -o {output}")

@jax.jit
def get_coevolution(X):
  '''given one-hot encoded MSA, return contacts'''
  Y = jax.nn.one_hot(X,22)
  N,L,A = Y.shape
  Y_flat = Y.reshape(N,-1)
  # covariance
  c = jnp.cov(Y_flat.T)

  # inverse covariance
  shrink = 4.5/jnp.sqrt(N) * jnp.eye(c.shape[0])
  ic = jnp.linalg.inv(c + shrink)

  # partial correlation coefficient
  ic_diag = jnp.diag(ic)
  pcc = ic / jnp.sqrt(ic_diag[:,None] * ic_diag[None,:])

  raw = jnp.sqrt(jnp.square(pcc.reshape(L,A,L,A)[:,:20,:,:20]).sum((1,3)))
  i = jnp.arange(L)
  raw = raw.at[i,i].set(0)
  # do apc
  ap = raw.sum(0,keepdims=True) * raw.sum(1,keepdims=True) / raw.sum()
  return (raw - ap).at[i,i].set(0)

def plot_3D(aux, Ls, file_name, show=False):
  plt.figure(figsize=(10,5))
  xyz = aux["atom_positions"][:,1]
  xyz = xyz @ _np_kabsch(xyz, xyz, return_v=True, use_jax=False)
  ax = plt.subplot(1,2,1)
  if len(Ls) > 1:
    plt.title("chain")
    c = np.concatenate([[n]*L for n,L in enumerate(Ls)])
    plot_pseudo_3D(xyz=xyz, c=c, cmap=pymol_cmap, cmin=0, cmax=39, Ls=Ls, ax=ax)
  else:
    plt.title("length")
    plot_pseudo_3D(xyz=xyz, Ls=Ls, ax=ax)
  plt.axis(False)
  ax = plt.subplot(1,2,2)
  plt.title("plddt")
  plot_pseudo_3D(xyz=xyz, c=aux["plddt"], cmin=0.5, cmax=0.9, Ls=Ls, ax=ax)
  plt.axis(False)
  plt.savefig(file_name, dpi=200, bbox_inches='tight')
  plt.show() if show else plt.close()

def clean_seq(sequence):
  sequence = sequence.upper()
  sequence = re.sub("[^A-Z:/()]", "", sequence.upper())
  sequence = re.sub("\(",":(", sequence)
  sequence = re.sub("\)","):", sequence)
  sequence = re.sub(":+",":",sequence)
  sequence = re.sub("/+","/",sequence)
  sequence = re.sub("^[:/]+","",sequence)
  sequence = re.sub("[:/]+$","",sequence)
  return sequence

def clean_job(jobname):
  jobname = re.sub(r'\W+', '', jobname)
  return jobname

class ColabFold:
  ##############################################################################
  # prep_inputs
  ##############################################################################
  def prep_inputs(self, sequence,
                  jobname="test",
                  copies=1,
                  # msa options
                  msa_method="mmseqs2", pair_mode="unpaired_paired",
                  # filtering options
                  cov=75,id=90,qid=0,do_not_filter=False,
                  # template options
                  template_mode="none", pdb="", chain="A", rm_template_seq=False,
                  propagate_to_copies=False, do_not_align=False):

    # filter options
    self._use_templates = template_mode in ["mmseqs2","custom"]
    self._rm_sidechain = self._rm_sequence = rm_template_seq

    # process sequence
    sequences = sequence.split(":")
    u_sequences = predict.get_unique_sequences(sequences)
    self._u_cyclic = [x.startswith("(") for x in u_sequences]
    self._u_sub_lengths = [[len(y) for y in x.split("/")] for x in u_sequences]
    u_sequences = [x.replace("(","").replace(")","").replace("/","") for x in u_sequences]
    if len(sequences) > len(u_sequences):
      print("WARNING: use copies to define homooligomers")
    self._u_lengths = [len(x) for x in u_sequences]
    sub_seq = "".join(u_sequences)
    seq = sub_seq * copies

    jobname = f"{jobname}_{predict.get_hash(seq)[:5]}"
    def check(folder): return os.path.exists(folder)
    if check(jobname):
      n = 0
      while check(f"{jobname}_{n}"): n += 1
      jobname = f"{jobname}_{n}"

    print("jobname",jobname)
    print(f"length={self._u_lengths} copies={copies}")

    self._input_opts = {
      "sequence":u_sequences,
      "copies":copies,
      "msa_method":msa_method,
      "pair_mode":pair_mode,
      "do_not_filter":do_not_filter,
      "cov":cov,
      "id":id,
      "template_mode":template_mode,
      "propagate_to_copies":propagate_to_copies,
    }

    # GET MSA
    os.makedirs(jobname, exist_ok=True)
    self._Ls = [len(x) for x in u_sequences]
    if msa_method == "mmseqs2":
      msa, deletion_matrix = predict.get_msa(u_sequences, jobname,
        mode=pair_mode,
        cov=cov, id=id, qid=qid, max_msa=4096,
        do_not_filter=do_not_filter,
        mmseqs2_fn=lambda *x: run_mmseqs2(*x, user_agent="colabdesign/gamma"),
        hhfilter_fn=run_hhfilter)

    elif msa_method == "single_sequence":
      with open(f"{jobname}/msa.a3m","w") as a3m:
        a3m.write(f">{jobname}\n{sub_seq}\n")
      msa, deletion_matrix = predict.parse_a3m(f"{jobname}/msa.a3m")

    else:
      msa_format = msa_method.split("_")[1]
      print(f"upload {msa_method}")
      msa_dict = files.upload()
      lines = []
      for k,v in msa_dict.items():
        lines += v.decode().splitlines()
      input_lines = []
      for line in lines:
        line = line.replace("\x00","")
        if len(line) > 0 and not line.startswith('#'):
          input_lines.append(line)
      with open(f"{jobname}/msa.{msa_format}","w") as msa:
        msa.write("\n".join(input_lines))
      if msa_format != "a3m":
        os.system(f"perl hhsuite/scripts/reformat.pl {msa_format} a3m {jobname}/msa.{msa_format} {jobname}/msa.a3m")
      if do_not_filter:
        os.system(f"hhfilter -qid 0 -id 100 -cov 0 -i {jobname}/msa.a3m -o {jobname}/msa.filt.a3m")
      else:
        os.system(f"hhfilter -qid {qid} -id {id} -cov {cov} -i {jobname}/msa.a3m -o {jobname}/msa.filt.a3m")
      msa, deletion_matrix = predict.parse_a3m(f"{jobname}/msa.filt.a3m")

    if len(msa) > 1:
      predict.plot_msa(msa, self._Ls)
      plt.savefig(f"{jobname}/msa_feats.png", dpi=200, bbox_inches='tight')
      plt.show()

    ##################
    if self._use_templates:
      print("aligning template")
      template_msa = f"{jobname}/msa.a3m"
      if template_mode == "mmseqs2":
        predict.get_msa(u_sequences, jobname,
          mode="unpaired",
          mmseqs2_fn=lambda *x: run_mmseqs2(*x, user_agent="colabdesign/gamma"),
          do_not_filter=True,
          do_not_return=True,
          output_a3m=f"{jobname}/msa_tmp.a3m")
        template_msa = f"{jobname}/msa_tmp.a3m"
        if not propagate_to_copies and copies > 1:
          new_msa = []
          with open(template_msa, "r") as handle:
            for line in handle:
              if not line.startswith(">"):
                new_msa.append(line.rstrip())
          with open(template_msa, "w") as handle:
            for n,seq in enumerate(new_msa):
              handle.write(f">{n}\n{seq*copies}\n")

        templates = {}
        print("ID\tpdb\tcid\tevalue")
        for line in open(f"{jobname}/msa/_env/pdb70.m8","r"):
          p = line.rstrip().split()
          M,target_id,qid,e_value = p[0],p[1],p[2],p[10]
          M = int(M)
          if M not in templates:
            templates[M] = []
          if len(templates[M]) < 4:
            print(f"{int(M)}\t{target_id}\t{qid}\t{e_value}")
            templates[M].append(target_id)
        if len(templates) == 0:
          self._use_templates = False
          print("ERROR: no templates found...")
        else:
          Ms = sorted(list(templates.keys()))
          pdbs,chains = [],[]
          for M in Ms:
            for n,target_id in enumerate(templates[M]):
              pdb_id,chain_id = target_id.split("_")
              if len(pdbs) < n+1:
                pdbs.append([])
                chains.append([])
              pdbs[n].append(pdb_id)
              chains[n].append(chain_id)
          print(pdbs)
      else:
        pdbs,chains = [pdb],[chain]

    if self._use_templates:
      self._input_opts.update({"pdbs":pdbs, "chains":chains})
      batches = []
      for pdb,chain in zip(pdbs,chains):
        query_seq = "".join(u_sequences)
        batch = predict.get_template_feats(pdb, chain,
          query_seq=query_seq,
          query_a3m=template_msa,
          copies=copies,
          propagate_to_copies=propagate_to_copies,
          use_seq=not self._rm_sequence,
          get_pdb_fn=get_pdb,
          align_fn=run_do_not_align if do_not_align else run_hhalign)
        batches.append(batch)

      # for display
      plt.figure(figsize=(3*len(batches),3))
      for n,batch in enumerate(batches):
        plt.subplot(1,len(batches),n+1)
        plt.title(f"template features {n+1}")
        dgram = batch["dgram"].argmax(-1).astype(float)
        dgram[batch["dgram"].sum(-1) == 0] = np.nan
        Ln = dgram.shape[0]
        plt.imshow(dgram, extent=(0, Ln, Ln, 0))
        predict.plot_ticks(self._Ls * copies)
      plt.savefig(f"{jobname}/template_feats.png", dpi=200, bbox_inches='tight')
      plt.show()
    else:
      batches = [None]

    ################

    self._sequence = sequence
    self._jobname = jobname
    self._msa = msa
    self._deletion_matrix = deletion_matrix
    self._batches = batches
    self._copies = copies

  ##############################################################################
  # prep_model
  ##############################################################################
  def prep_model(self,
    # model options
    model_type="auto",
    rank_by="auto",
    debug=False,
    use_initial_guess=False,
    use_initial_atom_pos=False,
    # msa options
    num_msa=512,
    num_extra_msa=1024,
    use_cluster_profile=True):
    multi = len(self._u_lengths) > 1 or self._copies > 1

    if model_type == "monomer (ptm)":
      use_multimer = False
      pseudo_multimer = False
    elif model_type == "multimer (v3)":
      use_multimer = True
      pseudo_multimer = False
    elif model_type == "pseudo_multimer (v3)":
      use_multimer = True
      pseudo_multimer = True
    elif multi:
      use_multimer = True
      pseudo_multimer = False
    else:
      use_multimer = False
      pseudo_multimer = False

    if rank_by == "auto":
      rank_by = "multi" if multi else "plddt"
    self._rank_by = rank_by

    self._model_opts = {
        "num_msa":num_msa,
        "num_extra_msa":num_extra_msa,
        "num_templates":len(self._batches),
        "use_cluster_profile":use_cluster_profile,
        "use_multimer":use_multimer,
        "pseudo_multimer":pseudo_multimer,
        "use_templates":self._use_templates,
        "use_batch_as_template":False,
        "use_dgram":True,
        "protocol":"hallucination",
        "best_metric":rank_by,
        "optimize_seq":False,
        "debug":debug,
        "clear_prev":False,
        "use_initial_guess":use_initial_guess,
        "use_initial_atom_pos":use_initial_atom_pos,
    }

    # initialize the model
    if hasattr(self,"af"):
      # reuse the model and/or params if already initialized
      if self._model_opts != self.__model_opts:
        if self._model_opts["use_multimer"] == self.af._args["use_multimer"] \
        and self._model_opts["use_templates"] == self.af._args["use_templates"]:
          old_params = dict(zip(self.af._model_names,self.af._model_params))
        else:
          print("loading alphafold params")
          old_params = {}
          clear_mem()
        self.af = mk_af_model(old_params=old_params,
                              use_mlm=True, # can be disabled later with 0% masking
                              **self._model_opts)
        self.__model_opts = predict.copy_dict(self._model_opts)
    else:
      print("loading alphafold params")
      self.af = mk_af_model(use_mlm=True, **self._model_opts)
      self.__model_opts = predict.copy_dict(self._model_opts)

    # prep inputs
    self.af.prep_inputs(self._u_lengths, copies=self._copies, seed=0)
    self._print_key = ["plddt","ptm"]
    if len(self.af._lengths) > 1: self._print_key += ["i_ptm", "multi"]

    # for contact map
    self.af.set_opt("con",cutoff=8.0)
    # set templates
    if self._use_templates:
      # interchain masking determined by dgram
      self.af._inputs["interchain_mask"] = np.full_like(self.af._inputs["interchain_mask"],True)
      for n,batch in enumerate(self._batches):
        self.af.set_template(batch=batch, n=n)
      self.af.set_opt("template",
                rm_sc=self._rm_sidechain,
                rm_seq=self._rm_sequence)
    # set msa
    self.af.set_msa(self._msa, self._deletion_matrix)

    # set chainbreaks
    L_prev = 0
    for n,l in enumerate(self._u_sub_lengths * self._copies):
      for L_i in l[:-1]:
        self.af._inputs["residue_index"][L_prev+L_i:] += 32
        L_prev += L_i
      L_prev += l[-1]

    # set cyclic constraints
    i_cyclic = [n for n, c in enumerate(self._u_cyclic * self._copies) if c]
    if len(i_cyclic) > 0:
      add_cyclic_offset(self.af,i_cyclic)
  #############################################
  # run_alphafold
  #############################################
  def run_alphafold(self,
    #model options
    model = "all",
    num_recycles = 6,
    recycle_early_stop_tolerance = 0.5,
    select_best_across_recycles = False,
    #stochastic options
    use_mlm = True,
    use_dropout = False,
    seed = 0,
    num_seeds = 1,
    #extras
    show_images = True,
  ):
    self._run_opts = {
      "seed":seed,
      "use_mlm":use_mlm,
      "use_dropout":use_dropout,
      "num_recycles":num_recycles,
      "model":model,
      "select_best_across_recycles":select_best_across_recycles,
      "recycle_early_stop_tolerance":recycle_early_stop_tolerance
    }

    # decide which models to use
    if model == "all": models = self.af._model_names
    else: models = [self.af._model_names[int(model) - 1]]

    # set options
    self.af.set_opt("mlm", replace_fraction=0.15 if use_mlm else 0.0)

    pdb_path = f"{self._jobname}/pdb"
    os.makedirs(pdb_path, exist_ok=True)

    # keep track of results
    self._info = []
    self.af._tmp = {"traj":{"seq":[],"xyz":[],"plddt":[],"pae":[]},
                     "log":[],"best":{}}

    # run
    print("running prediction")
    with open(f"{self._jobname}/log.txt","w") as handle:
      # go through all seeds
      seeds = list(range(seed,seed+num_seeds))
      for seed in seeds:
        self.af.set_seed(seed)
        # go through all models
        for model in models:
          recycle = 0
          self.af._inputs.pop("prev",None)
          stop_recycle = False
          prev_pos = None
          # go through all recycles
          while recycle < num_recycles + 1:
            print_str = f"seed={seed} model={model} recycle={recycle}"
            self.af.predict(dropout=use_dropout, models=[model], verbose=False)

            # set previous inputs
            self.af._inputs["prev"] = self.af.aux["prev"]
            if self.af._args["use_initial_atom_pos"]:
              self.af._inputs["initial_atom_pos"] = self.af.aux["atom_positions"]

            # save results
            if len(self.af._lengths) > 1:
              self.af.aux["log"]["multi"] = 0.8 * self.af.aux["log"]["i_ptm"] + 0.2 * self.af.aux["log"]["ptm"]
            self.af.save_current_pdb(f"{pdb_path}/{model}_r{recycle}_seed{seed}.pdb")

            # print metrics
            for k in self._print_key: print_str += f" {k}={self.af.aux['log'][k]:.3f}"

            # early stop check
            current_pos = self.af.aux["atom_positions"][:,1]
            if recycle > 0:
              rmsd_tol = _np_rmsd(prev_pos, current_pos, use_jax=False)
              if rmsd_tol < recycle_early_stop_tolerance:
                stop_recycle = True
              print_str += f" rmsd_tol={rmsd_tol:.3f}"
            prev_pos = current_pos
            # print metrics
            print(print_str); handle.write(f"{print_str}\n")

            tag = f"{model}_r{recycle}_seed{seed}"
            if select_best_across_recycles:
              self._info.append([tag,print_str,self.af.aux["log"][self._rank_by]])
              self.af._save_results(save_best=True,
                best_metric=self._rank_by, metric_higher_better=True,
                verbose=False)
              self.af._k += 1

            recycle += 1
            if stop_recycle: break

          if not select_best_across_recycles:
            self._info.append([tag,print_str, self.af.aux["log"][self._rank_by]])
            self.af._save_results(save_best=True,
                            best_metric=self._rank_by, metric_higher_better=True,
                            verbose=False)
            self.af._k += 1

          # save current results
          plot_3D(self.af.aux, self._Ls * self._copies, f"{pdb_path}/{model}_seed{seed}.pdf", show=show_images)
          predict.plot_confidence(self.af.aux["plddt"]*100, self.af.aux["pae"], self._Ls * self._copies)
          plt.savefig(f"{pdb_path}/{model}_seed{seed}.png", dpi=200, bbox_inches='tight')
          plt.close()

    # save best results
    rank = np.argsort([x[2] for x in self._info])[::-1][:5]
    print(f"best_tag={self._info[rank[0]][0]} {self._info[rank[0]][1]}")

    self._aux_best = self.af._tmp["best"]["aux"]
    self.af.save_pdb(f"{pdb_path}/best.pdb")
    np.savez_compressed(f"{pdb_path}/best.npz",
                        plddt=self._aux_best["plddt"].astype(np.float16),
                        pae=self._aux_best["pae"].astype(np.float16),
                        tag=np.array(self._info[rank[0]][0]),
                        metrics=np.array(self._info[rank[0]][1]))
    np.savez_compressed(f"{pdb_path}/all.npz",
                        plddt=np.array(self.af._tmp["traj"]["plddt"], dtype=np.float16),
                        pae=np.array(self.af._tmp["traj"]["pae"], dtype=np.float16),
                        tag=np.array([x[0] for x in self._info]),
                        metrics=np.array([x[1] for x in self._info]))
    plot_3D(self._aux_best, self._Ls * self._copies, f"{pdb_path}/best.pdf", show=False)
    predict.plot_confidence(self._aux_best["plddt"]*100, self._aux_best["pae"], self._Ls * self._copies)
    plt.savefig(f"{pdb_path}/best.png", dpi=200, bbox_inches='tight')
    plt.close()

# initialize
cf = ColabFold()












#@title prep_inputs
sequence = "MAAVTGIALGMIETRGLVPAIEAADAMTKAAEVRLVGRQFVGGGYVTVLVRGETGAVNAAVRAGADACERVGDGLVAAHIIARVHSEVENILPKAPEA" #@param {type:"string"}
jobname = "test" #@param {type:"string"}

sequence = clean_seq(sequence)
jobname = clean_job(jobname)

#@title run_initial_prediction
model_type = "monomer (ptm)" #@param ["monomer (ptm)", "pseudo_multimer (v3)", "multimer (v3)"]
model = "1" #@param ["1", "2", "3", "4", "5", "all"]
ini_copies = 2
cf.prep_inputs(sequence=sequence, jobname=jobname, copies=ini_copies)
cf.prep_model(model_type=model_type)
cf.run_alphafold(model=model)
ini_jobname = cf._jobname
gc.collect()

#@title find_symmetry
method = "make_symmdef" #@param ["AnAnaS", "make_symmdef"]

from string import ascii_uppercase
import json
import subprocess
ini_pdb = f"{ini_jobname}/pdb/best.pdb"

if method == "AnAnaS":
  sym_pdb = f"{ini_jobname}/pdb/sym.pdb"
  sym_json = f"{ini_jobname}/pdb/sym.json"

  best_rmsd = None
  best_k = None
  for k in range(2,13):
    cmd = f"./ananas {ini_pdb} c{k} -C 100"
    rmsd = float(subprocess.getoutput(cmd).split("Average RMSD")[1].split()[1])
    print(f"c{k} rmsd={rmsd:.3}")
    if best_rmsd is None or rmsd < best_rmsd:
      best_rmsd = rmsd
      best_k = k

  cmd = f"./ananas {ini_pdb} c{best_k} -C 100 --symmetrize {sym_pdb} --json {sym_json}"
  os.system(cmd)
  results = json.loads(open(sym_json,"r").read())
  group = results[0]["group"]
  rmsd = results[0]["Average_RMSD"]
  print(f"AnAnaS detected {group} symmetry at RMSD:{rmsd:.3}")

if method == "make_symmdef":
  sym_pdb = f"{ini_jobname}/pdb/best_symm.pdb"
  sym_def = f"{ini_jobname}/pdb/best_symm.txt"
  sym_log = f"{ini_jobname}/pdb/best_symm.log.txt"
  cmd = f"perl make_symmdef_file.pl -m NCS -p {ini_pdb} 2> {sym_log} 1> {sym_def}"
  os.system(cmd)
  for line in open(sym_log,"r").readlines():
    print(line.rstrip())

copies = !grep TER {sym_pdb} | wc -l
copies = int(copies[0])

#@title run_final_prediction
model_type = "monomer (ptm)" #@param ["monomer (ptm)", "pseudo_multimer (v3)", "multimer (v3)"]
#sym_method = "ananas" #@param ["ananas", "symmdef"]
model = "1" #@param ["1", "2", "3", "4", "5", "all"]

cf.prep_inputs(sequence=sequence,
               msa_method="single_sequence",
               template_mode="custom",
               pdb=sym_pdb,
               chain=",".join(list(ascii_uppercase[:copies])),
               jobname=jobname,
               copies=copies,
               do_not_align=True,
               propagate_to_copies=False,
               rm_template_seq=True)

cf.prep_model(model_type=model_type,
              use_initial_atom_pos=True)

# center coordinates (not sure if this is needed)
ini_pos = cf.af._inputs["template_all_atom_positions"][0]
cf.af._inputs["template_all_atom_positions"][0] -= ini_pos[:,1].mean(0)

cf.run_alphafold(model=model)

#@title display_best_result (optional) {run: "auto"}
color = "pLDDT" #@param ["pLDDT","chain","rainbow"]
show_sidechains = False #@param {type:"boolean"}
show_mainchains = False #@param {type:"boolean"}
color_HP = True

cf.af.plot_pdb(color=color, show_sidechains=show_sidechains, show_mainchains=show_mainchains, color_HP=color_HP)
predict.plot_plddt_legend().show()
if not hasattr(cf,"_aux_best"):
  cf._aux_best = cf.af._tmp["best"]["aux"]
predict.plot_confidence(cf._aux_best["plddt"]*100, cf._aux_best["pae"], cf._u_lengths * cf._copies).show()

#@title download_prediction

#@markdown Once this cell has been executed, a zip-archive with
#@markdown the obtained prediction will be automatically downloaded
#@markdown to your computer.

# add settings file
settings_path = f"{cf._jobname}/settings.txt"
with open(settings_path, "w") as text_file:
  if hasattr(cf,"_input_opts"):
    for k,v in cf._input_opts.items():
      text_file.write(f"{k}={v}\n")
  if hasattr(cf,"_model_opts"):
    for k,v in cf._model_opts.items():
      text_file.write(f"{k}={v}\n")
  if hasattr(cf,"_run_opts"):
    for k,v in cf._run_opts.items():
      text_file.write(f"{k}={v}\n")
# --- Download the predictions ---
os.system(f"zip -r {cf._jobname}.zip {cf._jobname}")
files.download(f'{cf._jobname}.zip')


