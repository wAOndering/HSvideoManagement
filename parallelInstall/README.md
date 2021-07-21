
*USE GitBash
*USE GNU parralel
*USE ffmpeg


install gitBash
install GNU parallel
	* https://git.savannah.gnu.org/cgit/parallel.git/plain/10seconds_install
	* https://www.gnu.org/software/parallel/checksums/

Details for GNU parallel install and see below
1. in GitBash input:
$ (wget -O - pi.dk/3 || lynx -source pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) > install.sh
$ sha1sum install.sh | grep 12345678
$ md5sum install.sh
$ sha512sum install.sh
$ bash install.sh


usage of GNU parallel



Note from paralllel:

Academic tradition requires you to cite works you base your article on.
If you use programs that use GNU Parallel to process data for an article in
scientific publication, please cite:

  Tange, O. (2021, June 22). GNU Parallel 20210622 ('Protasevich').
  Zenodo. https://doi.org/10.5281/zenodo.5013933

This helps funding further development; AND IT WON'T COST YOU A CENT.
If you pay 10000 EUR you should feel free to use GNU Parallel without citing

More about funding GNU Parallel and the citation notice:
https://www.gnu.org/software/parallel/parallel_design.html#Citation-notice
