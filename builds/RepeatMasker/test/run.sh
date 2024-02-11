

./rename_sequences.py -i test/test.fa -o test/test.rn.fa -f test/test.fromto.txt 
./unrename_sequences.py -i test/test.rn.fa -o test/test.rn.rn.fa -f test/test.fromto.txt -t fasta
./unrename_sequences.py -i test/test.gff -o test/test.rn.gff -f test/test.fromto.txt -t gff


./unrename_sequences.py -i test/test.bad.fa -o test/test.bad.rn.fa -f test/test.fromto.txt -t fasta
./unrename_sequences.py -i test/test.bad.gff -o test/test.bad.rn.gff -f test/test.fromto.txt -t gff

