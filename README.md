# proiect_pdd


pip install faker mysql-connector-python psycopg2-binary



burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo apt update
Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
Hit:2 http://archive.ubuntu.com/ubuntu jammy InRelease                                                                                                                       
Get:3 http://apt.postgresql.org/pub/repos/apt jammy-pgdg InRelease [180 kB]                                                                                                  
Get:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]                                                                                                      
Hit:5 https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 InRelease                                                                                                   
Get:6 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease [18.1 kB]                                                                       
Get:8 http://apt.postgresql.org/pub/repos/apt jammy-pgdg/main amd64 Packages [573 kB]                                                  
Hit:7 https://apt.llvm.org/jammy llvm-toolchain-jammy-19 InRelease                                
Get:9 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]                         
Get:10 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy/main amd64 Packages [33.0 kB]
Get:11 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [3265 kB]
Get:12 http://security.ubuntu.com/ubuntu jammy-security/main Translation-en [460 kB]
Get:13 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [5819 kB]
Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [3539 kB]
Get:15 http://security.ubuntu.com/ubuntu jammy-security/restricted Translation-en [1113 kB]   
Get:16 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1035 kB]          
Get:17 http://security.ubuntu.com/ubuntu jammy-security/universe Translation-en [229 kB]     
Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/main Translation-en [532 kB]                 
Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 c-n-f Metadata [19.9 kB]
Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [6040 kB]
Get:21 http://archive.ubuntu.com/ubuntu jammy-updates/restricted Translation-en [1154 kB]
Get:22 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1273 kB]
Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/universe Translation-en [318 kB]
Fetched 26.0 MB in 6s (4707 kB/s)                                       
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
69 packages can be upgraded. Run 'apt list --upgradable' to see them.
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo apt install mysql-server -y~
E: Command line option '~' [from -y~] is not understood in combination with the other options.
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo apt install mysql-server -y
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  golang-1.18-go golang-1.18-src golang-src htop libnl-3-200 libnl-genl-3-200
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  libaio1 libcgi-fast-perl libcgi-pm-perl libevent-pthreads-2.1-7 libfcgi-bin libfcgi-perl libfcgi0ldbl libhtml-template-perl libmecab2 libprotobuf-lite23 mecab-ipadic
  mecab-ipadic-utf8 mecab-utils mysql-client-8.0 mysql-client-core-8.0 mysql-common mysql-server-8.0 mysql-server-core-8.0
Suggested packages:
  libipc-sharedcache-perl mailx tinyca
The following NEW packages will be installed:
  libaio1 libcgi-fast-perl libcgi-pm-perl libevent-pthreads-2.1-7 libfcgi-bin libfcgi-perl libfcgi0ldbl libhtml-template-perl libmecab2 libprotobuf-lite23 mecab-ipadic
  mecab-ipadic-utf8 mecab-utils mysql-client-8.0 mysql-client-core-8.0 mysql-common mysql-server mysql-server-8.0 mysql-server-core-8.0
0 upgraded, 19 newly installed, 0 to remove and 69 not upgraded.
Need to get 29.5 MB of archives.
After this operation, 243 MB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu jammy/main amd64 mysql-common all 5.8+1.0.8 [7212 B]
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mysql-client-core-8.0 amd64 8.0.46-0ubuntu0.22.04.2 [2742 kB]
Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mysql-client-8.0 amd64 8.0.46-0ubuntu0.22.04.2 [22.7 kB]
Get:4 http://archive.ubuntu.com/ubuntu jammy/main amd64 libaio1 amd64 0.3.112-13build1 [7176 B]
Get:5 http://archive.ubuntu.com/ubuntu jammy/main amd64 libevent-pthreads-2.1-7 amd64 2.1.12-stable-1build3 [7642 B]
Get:6 http://archive.ubuntu.com/ubuntu jammy/main amd64 libmecab2 amd64 0.996-14build9 [199 kB]
Get:7 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libprotobuf-lite23 amd64 3.12.4-1ubuntu7.22.04.6 [209 kB]
Get:8 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mysql-server-core-8.0 amd64 8.0.46-0ubuntu0.22.04.2 [17.8 MB]
Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mysql-server-8.0 amd64 8.0.46-0ubuntu0.22.04.2 [1451 kB]
Get:10 http://archive.ubuntu.com/ubuntu jammy/main amd64 libcgi-pm-perl all 4.54-1 [188 kB]
Get:11 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libfcgi0ldbl amd64 2.4.2-2ubuntu0.1 [28.1 kB]
Get:12 http://archive.ubuntu.com/ubuntu jammy/main amd64 libfcgi-perl amd64 0.82+ds-1build1 [22.8 kB]
Get:13 http://archive.ubuntu.com/ubuntu jammy/main amd64 libcgi-fast-perl all 1:2.15-1 [10.5 kB]
Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libfcgi-bin amd64 2.4.2-2ubuntu0.1 [11.1 kB]
Get:15 http://archive.ubuntu.com/ubuntu jammy/main amd64 libhtml-template-perl all 2.97-1.1 [59.1 kB]
Get:16 http://archive.ubuntu.com/ubuntu jammy/main amd64 mecab-utils amd64 0.996-14build9 [4850 B]
Get:17 http://archive.ubuntu.com/ubuntu jammy/main amd64 mecab-ipadic all 2.7.0-20070801+main-3 [6718 kB]
Get:18 http://archive.ubuntu.com/ubuntu jammy/main amd64 mecab-ipadic-utf8 all 2.7.0-20070801+main-3 [4384 B]
Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mysql-server all 8.0.46-0ubuntu0.22.04.2 [9458 B]
Fetched 29.5 MB in 1s (40.2 MB/s)      
Preconfiguring packages ...
Selecting previously unselected package mysql-common.
(Reading database ... 92711 files and directories currently installed.)
Preparing to unpack .../0-mysql-common_5.8+1.0.8_all.deb ...
Unpacking mysql-common (5.8+1.0.8) ...
Selecting previously unselected package mysql-client-core-8.0.
Preparing to unpack .../1-mysql-client-core-8.0_8.0.46-0ubuntu0.22.04.2_amd64.deb ...
Unpacking mysql-client-core-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Selecting previously unselected package mysql-client-8.0.
Preparing to unpack .../2-mysql-client-8.0_8.0.46-0ubuntu0.22.04.2_amd64.deb ...
Unpacking mysql-client-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Selecting previously unselected package libaio1:amd64.
Preparing to unpack .../3-libaio1_0.3.112-13build1_amd64.deb ...
Unpacking libaio1:amd64 (0.3.112-13build1) ...
Selecting previously unselected package libevent-pthreads-2.1-7:amd64.
Preparing to unpack .../4-libevent-pthreads-2.1-7_2.1.12-stable-1build3_amd64.deb ...
Unpacking libevent-pthreads-2.1-7:amd64 (2.1.12-stable-1build3) ...
Selecting previously unselected package libmecab2:amd64.
Preparing to unpack .../5-libmecab2_0.996-14build9_amd64.deb ...
Unpacking libmecab2:amd64 (0.996-14build9) ...
Selecting previously unselected package libprotobuf-lite23:amd64.
Preparing to unpack .../6-libprotobuf-lite23_3.12.4-1ubuntu7.22.04.6_amd64.deb ...
Unpacking libprotobuf-lite23:amd64 (3.12.4-1ubuntu7.22.04.6) ...
Selecting previously unselected package mysql-server-core-8.0.
Preparing to unpack .../7-mysql-server-core-8.0_8.0.46-0ubuntu0.22.04.2_amd64.deb ...
Unpacking mysql-server-core-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Setting up mysql-common (5.8+1.0.8) ...
update-alternatives: using /etc/mysql/my.cnf.fallback to provide /etc/mysql/my.cnf (my.cnf) in auto mode
Selecting previously unselected package mysql-server-8.0.
(Reading database ... 92930 files and directories currently installed.)
Preparing to unpack .../00-mysql-server-8.0_8.0.46-0ubuntu0.22.04.2_amd64.deb ...
Unpacking mysql-server-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Selecting previously unselected package libcgi-pm-perl.
Preparing to unpack .../01-libcgi-pm-perl_4.54-1_all.deb ...
Unpacking libcgi-pm-perl (4.54-1) ...
Selecting previously unselected package libfcgi0ldbl:amd64.
Preparing to unpack .../02-libfcgi0ldbl_2.4.2-2ubuntu0.1_amd64.deb ...
Unpacking libfcgi0ldbl:amd64 (2.4.2-2ubuntu0.1) ...
Selecting previously unselected package libfcgi-perl:amd64.
Preparing to unpack .../03-libfcgi-perl_0.82+ds-1build1_amd64.deb ...
Unpacking libfcgi-perl:amd64 (0.82+ds-1build1) ...
Selecting previously unselected package libcgi-fast-perl.
Preparing to unpack .../04-libcgi-fast-perl_1%3a2.15-1_all.deb ...
Unpacking libcgi-fast-perl (1:2.15-1) ...
Selecting previously unselected package libfcgi-bin.
Preparing to unpack .../05-libfcgi-bin_2.4.2-2ubuntu0.1_amd64.deb ...
Unpacking libfcgi-bin (2.4.2-2ubuntu0.1) ...
Selecting previously unselected package libhtml-template-perl.
Preparing to unpack .../06-libhtml-template-perl_2.97-1.1_all.deb ...
Unpacking libhtml-template-perl (2.97-1.1) ...
Selecting previously unselected package mecab-utils.
Preparing to unpack .../07-mecab-utils_0.996-14build9_amd64.deb ...
Unpacking mecab-utils (0.996-14build9) ...
Selecting previously unselected package mecab-ipadic.
Preparing to unpack .../08-mecab-ipadic_2.7.0-20070801+main-3_all.deb ...
Unpacking mecab-ipadic (2.7.0-20070801+main-3) ...
Selecting previously unselected package mecab-ipadic-utf8.
Preparing to unpack .../09-mecab-ipadic-utf8_2.7.0-20070801+main-3_all.deb ...
Unpacking mecab-ipadic-utf8 (2.7.0-20070801+main-3) ...
Selecting previously unselected package mysql-server.
Preparing to unpack .../10-mysql-server_8.0.46-0ubuntu0.22.04.2_all.deb ...
Unpacking mysql-server (8.0.46-0ubuntu0.22.04.2) ...
Setting up libmecab2:amd64 (0.996-14build9) ...
Setting up mysql-client-core-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Setting up libfcgi0ldbl:amd64 (2.4.2-2ubuntu0.1) ...
Setting up libcgi-pm-perl (4.54-1) ...
Setting up libfcgi-bin (2.4.2-2ubuntu0.1) ...
Setting up libhtml-template-perl (2.97-1.1) ...
Setting up libprotobuf-lite23:amd64 (3.12.4-1ubuntu7.22.04.6) ...
Setting up mecab-utils (0.996-14build9) ...
Setting up mysql-client-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Setting up libfcgi-perl:amd64 (0.82+ds-1build1) ...
Setting up libaio1:amd64 (0.3.112-13build1) ...
Setting up libevent-pthreads-2.1-7:amd64 (2.1.12-stable-1build3) ...
Setting up mecab-ipadic (2.7.0-20070801+main-3) ...
Compiling IPA dictionary for Mecab.  This takes long time...
reading /usr/share/mecab/dic/ipadic/unk.def ... 40
emitting double-array: 100% |###########################################| 
/usr/share/mecab/dic/ipadic/model.def is not found. skipped.
reading /usr/share/mecab/dic/ipadic/Adj.csv ... 27210
reading /usr/share/mecab/dic/ipadic/Filler.csv ... 19
reading /usr/share/mecab/dic/ipadic/Noun.verbal.csv ... 12146
reading /usr/share/mecab/dic/ipadic/Verb.csv ... 130750
reading /usr/share/mecab/dic/ipadic/Noun.nai.csv ... 42
reading /usr/share/mecab/dic/ipadic/Adnominal.csv ... 135
reading /usr/share/mecab/dic/ipadic/Noun.adjv.csv ... 3328
reading /usr/share/mecab/dic/ipadic/Noun.name.csv ... 34202
reading /usr/share/mecab/dic/ipadic/Noun.proper.csv ... 27328
reading /usr/share/mecab/dic/ipadic/Conjunction.csv ... 171
reading /usr/share/mecab/dic/ipadic/Noun.demonst.csv ... 120
reading /usr/share/mecab/dic/ipadic/Adverb.csv ... 3032
reading /usr/share/mecab/dic/ipadic/Others.csv ... 2
reading /usr/share/mecab/dic/ipadic/Noun.number.csv ... 42
reading /usr/share/mecab/dic/ipadic/Suffix.csv ... 1393
reading /usr/share/mecab/dic/ipadic/Interjection.csv ... 252
reading /usr/share/mecab/dic/ipadic/Auxil.csv ... 199
reading /usr/share/mecab/dic/ipadic/Noun.adverbal.csv ... 795
reading /usr/share/mecab/dic/ipadic/Noun.place.csv ... 72999
reading /usr/share/mecab/dic/ipadic/Prefix.csv ... 221
reading /usr/share/mecab/dic/ipadic/Postp-col.csv ... 91
reading /usr/share/mecab/dic/ipadic/Symbol.csv ... 208
reading /usr/share/mecab/dic/ipadic/Postp.csv ... 146
reading /usr/share/mecab/dic/ipadic/Noun.org.csv ... 16668
reading /usr/share/mecab/dic/ipadic/Noun.others.csv ... 151
reading /usr/share/mecab/dic/ipadic/Noun.csv ... 60477
emitting double-array: 100% |###########################################| 
reading /usr/share/mecab/dic/ipadic/matrix.def ... 1316x1316
emitting matrix      : 100% |###########################################| 

done!
update-alternatives: using /var/lib/mecab/dic/ipadic to provide /var/lib/mecab/dic/debian (mecab-dictionary) in auto mode
Setting up libcgi-fast-perl (1:2.15-1) ...
Setting up mysql-server-core-8.0 (8.0.46-0ubuntu0.22.04.2) ...
Setting up mecab-ipadic-utf8 (2.7.0-20070801+main-3) ...
Compiling IPA dictionary for Mecab.  This takes long time...
reading /usr/share/mecab/dic/ipadic/unk.def ... 40
emitting double-array: 100% |###########################################| 
/usr/share/mecab/dic/ipadic/model.def is not found. skipped.
reading /usr/share/mecab/dic/ipadic/Adj.csv ... 27210
reading /usr/share/mecab/dic/ipadic/Filler.csv ... 19
reading /usr/share/mecab/dic/ipadic/Noun.verbal.csv ... 12146
reading /usr/share/mecab/dic/ipadic/Verb.csv ... 130750
reading /usr/share/mecab/dic/ipadic/Noun.nai.csv ... 42
reading /usr/share/mecab/dic/ipadic/Adnominal.csv ... 135
reading /usr/share/mecab/dic/ipadic/Noun.adjv.csv ... 3328
reading /usr/share/mecab/dic/ipadic/Noun.name.csv ... 34202
reading /usr/share/mecab/dic/ipadic/Noun.proper.csv ... 27328
reading /usr/share/mecab/dic/ipadic/Conjunction.csv ... 171
reading /usr/share/mecab/dic/ipadic/Noun.demonst.csv ... 120
reading /usr/share/mecab/dic/ipadic/Adverb.csv ... 3032
reading /usr/share/mecab/dic/ipadic/Others.csv ... 2
reading /usr/share/mecab/dic/ipadic/Noun.number.csv ... 42
reading /usr/share/mecab/dic/ipadic/Suffix.csv ... 1393
reading /usr/share/mecab/dic/ipadic/Interjection.csv ... 252
reading /usr/share/mecab/dic/ipadic/Auxil.csv ... 199
reading /usr/share/mecab/dic/ipadic/Noun.adverbal.csv ... 795
reading /usr/share/mecab/dic/ipadic/Noun.place.csv ... 72999
reading /usr/share/mecab/dic/ipadic/Prefix.csv ... 221
reading /usr/share/mecab/dic/ipadic/Postp-col.csv ... 91
reading /usr/share/mecab/dic/ipadic/Symbol.csv ... 208
reading /usr/share/mecab/dic/ipadic/Postp.csv ... 146
reading /usr/share/mecab/dic/ipadic/Noun.org.csv ... 16668
reading /usr/share/mecab/dic/ipadic/Noun.others.csv ... 151
reading /usr/share/mecab/dic/ipadic/Noun.csv ... 60477
emitting double-array: 100% |###########################################| 
reading /usr/share/mecab/dic/ipadic/matrix.def ... 1316x1316
emitting matrix      : 100% |###########################################| 

done!
update-alternatives: using /var/lib/mecab/dic/ipadic-utf8 to provide /var/lib/mecab/dic/debian (mecab-dictionary) in auto mode
Setting up mysql-server-8.0 (8.0.46-0ubuntu0.22.04.2) ...
update-alternatives: using /etc/mysql/mysql.cnf to provide /etc/mysql/my.cnf (my.cnf) in auto mode
Renaming removed key_buffer and myisam-recover options (if present)
mysqld will log errors to /var/log/mysql/error.log
mysqld is running as pid 2528
Created symlink /etc/systemd/system/multi-user.target.wants/mysql.service → /lib/systemd/system/mysql.service.
Setting up mysql-server (8.0.46-0ubuntu0.22.04.2) ...
Processing triggers for man-db (2.10.2-1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.13) ...
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo service mysql start
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo service mysql status
● mysql.service - MySQL Community Server
     Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2026-06-03 21:08:21 EEST; 13s ago
    Process: 2725 ExecStartPre=/usr/share/mysql/mysql-systemd-start pre (code=exited, status=0/SUCCESS)
   Main PID: 2744 (mysqld)
     Status: "Server is operational"
      Tasks: 38 (limit: 16650)
     Memory: 371.8M
     CGroup: /system.slice/mysql.service
             └─2744 /usr/sbin/mysqld

Jun 03 21:08:20 DESKTOP-TDTDREU systemd[1]: Starting MySQL Community Server...
Jun 03 21:08:21 DESKTOP-TDTDREU systemd[1]: Started MySQL Community Server.
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.46-0ubuntu0.22.04.2 (Ubuntu)

Copyright (c) 2000, 2026, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE benchmark_db;
EATE USER 'benchmark_user'@'localhost' IDENTIFIED BY 'benchmark_pass';
GRANT ALL PRIVILEGES ON benchmark_db.* TO 'benchmark_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;Query OK, 1 row affected (0.03 sec)

mysql> CREATE USER 'benchmark_user'@'localhost' IDENTIFIED BY 'benchmark_pass';
Query OK, 0 rows affected (0.04 sec)

mysql> GRANT ALL PRIVILEGES ON benchmark_db.* TO 'benchmark_user'@'localhost';
Query OK, 0 rows affected (0.01 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> EXIT;
Bye

burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo service postgresql start
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo -u postgres psql
psql (18.1 (Ubuntu 18.1-1.pgdg22.04+2))
Type "help" for help.

postgres=# CREATE DATABASE benchmark_db;
CREATE USER benchmark_user WITH PASSWORD 'benchmark_pass';
GRANT ALL PRIVILEGES ON DATABASE benchmark_db TO benchmark_user;
\c benchmark_db
GRANT ALL ON SCHEMA public TO benchmark_user;
\q
CREATE DATABASE
CREATE ROLE
GRANT
invalid integer value "ON" for connection option "port"
Previous connection kept
postgres=# ^C
postgres=# q
postgres-# exit
Use \q to quit.
postgres-# \q
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ sudo -u postgres psql -d benchmark_db
psql (18.1 (Ubuntu 18.1-1.pgdg22.04+2))
Type "help" for help.

benchmark_db=# GRANT ALL ON SCHEMA public TO benchmark_user;
GRANT
benchmark_db=# \q
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ mysql -u benchmark_user -pbenchmark_pass benchmark_db -e "SELECT 'MySQL OK';"
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| MySQL OK |
+----------+
| MySQL OK |
+----------+
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ psql -U benchmark_user -d benchmark_db -h 127.0.0.1 -c "SELECT 'PostgreSQL OK';"
Password for user benchmark_user: 
psql: error: connection to server at "127.0.0.1", port 5432 failed: FATAL:  password authentication failed for user "benchmark_user"
connection to server at "127.0.0.1", port 5432 failed: FATAL:  password authentication failed for user "benchmark_user"
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ psql -U benchmark_user -d benchmark_db -h 127.0.0.1 -c "SELECT 'PostgreSQL OK';"
Password for user benchmark_user: 
   ?column?    
---------------
 PostgreSQL OK
(1 row)



pip install faker mysql-connector-python psycopg2-binary pandas matplotlib



# Doar SQLite (cel mai simplu, fără server necesar)
python3 generate_data.py --sqlite

# Doar MySQL (server-ul trebuie pornit)
python3 generate_data.py --mysql

# Doar PostgreSQL
python3 generate_data.py --postgres

# Toate trei
python generate_data.py --all

# Pe un terminal 
python3 sqlite_server.py

# Pe altul:


touch metrics.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ touch client_mysql.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ touch client_postgresql.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ touch client_sqlite.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ touch benchmark.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ touch report.py
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 benchmark.py 
Starting benchmark suite...
Databases: MySQL 8.0 | PostgreSQL 18 | SQLite 3.45
Scenarios: INSERT(1K/10K/100K) | SELECT | JOIN | AGGREGATION | UPDATE/DELETE
Runs per scenario: 5\n
\n=== Connection Overhead (5 measurements each) ===
  mysql         mean=  31.72ms  std= 49.91ms
  postgresql    mean=  28.48ms  std= 31.84ms
  sqlite        mean=  38.68ms  std=  9.97ms
\n=== MySQL ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  MySQL done ✓
\n=== PostgreSQL ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  PostgreSQL done ✓
\n=== SQLite ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  SQLite done ✓
\n================================================================================
DB             Scenario                Mean (ms)   Std (ms)   Runs
================================================================================
mysql          bulk_insert_1000           200.22     189.77      5
mysql          bulk_insert_10000          554.02     112.76      5
mysql          bulk_insert_100000        7136.10     329.52      5
mysql          select_where                 4.89       6.36      5
mysql          complex_join                 7.42       1.91      5
mysql          aggregation               4284.37    1218.62      5
mysql          update_delete              622.96      33.41      5
postgresql     bulk_insert_1000           111.71     142.35      5
postgresql     bulk_insert_10000          491.13      58.49      5
postgresql     bulk_insert_100000        4617.31     182.30      5
postgresql     select_where                 7.52      14.28      5
postgresql     complex_join                12.45      10.00      5
postgresql     aggregation                216.11      35.78      5
postgresql     update_delete              790.96    1060.50      5
sqlite         bulk_insert_1000           460.73      18.38      5
sqlite         bulk_insert_10000         4319.79     145.31      5
sqlite         bulk_insert_100000       49946.39     274.39      5
sqlite         select_where                 3.43       3.99      5
sqlite         complex_join               421.55      14.90      5
sqlite         aggregation              93257.98    3476.31      5
sqlite         update_delete            10904.30    6470.98      5
================================================================================
\nResults saved to results.csv
\nDone! Run report.py to generate charts.




burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ pip install plotly kaleido
Defaulting to user installation because normal site-packages is not writeable
Collecting plotly
  Downloading plotly-6.8.0-py3-none-any.whl.metadata (9.0 kB)
Collecting kaleido
  Downloading kaleido-1.3.0-py3-none-any.whl.metadata (5.6 kB)
Requirement already satisfied: narwhals>=1.15.1 in /home/burak/.local/lib/python3.10/site-packages (from plotly) (2.12.0)
Requirement already satisfied: packaging in /home/burak/.local/lib/python3.10/site-packages (from plotly) (24.1)
Collecting choreographer>=1.3.0 (from kaleido)
  Downloading choreographer-1.3.0-py3-none-any.whl.metadata (6.9 kB)
Collecting logistro>=1.0.8 (from kaleido)
  Downloading logistro-2.0.1-py3-none-any.whl.metadata (3.9 kB)
Requirement already satisfied: orjson>=3.10.15 in /home/burak/.local/lib/python3.10/site-packages (from kaleido) (3.10.18)
Collecting platformdirs>=4.3.6 (from choreographer>=1.3.0->kaleido)
  Downloading platformdirs-4.10.0-py3-none-any.whl.metadata (5.5 kB)
Collecting simplejson>=3.19.3 (from choreographer>=1.3.0->kaleido)
  Downloading simplejson-4.1.1-cp310-cp310-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.8 kB)
Downloading plotly-6.8.0-py3-none-any.whl (9.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.9/9.9 MB 24.6 MB/s  0:00:00
Downloading kaleido-1.3.0-py3-none-any.whl (55 kB)
Downloading choreographer-1.3.0-py3-none-any.whl (52 kB)
Downloading logistro-2.0.1-py3-none-any.whl (8.6 kB)
Downloading platformdirs-4.10.0-py3-none-any.whl (22 kB)
Downloading simplejson-4.1.1-cp310-cp310-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (168 kB)
Installing collected packages: simplejson, plotly, platformdirs, logistro, choreographer, kaleido
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
virtualenv 20.13.0+ds requires platformdirs<3,>=2, but you have platformdirs 4.10.0 which is incompatible.
Successfully installed choreographer-1.3.0 kaleido-1.3.0 logistro-2.0.1 platformdirs-4.10.0 plotly-6.8.0 simplejson-4.1.1

[notice] A new release of pip is available: 26.0.1 -> 26.1.2
[notice] To update, run: python3 -m pip install --upgrade pip
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ which python3
/usr/bin/python3
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 --version
Python 3.10.12
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 -m pip --version
pip 26.0.1 from /home/burak/.local/lib/python3.10/site-packages/pip (python 3.10)
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ pip --version
pip 26.0.1 from /home/burak/.local/lib/python3.10/site-packages/pip (python 3.10)
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 -c "import sys; print(sys.executable); print('\n'.join(sys.path))"
/usr/bin/python3

/usr/lib/python310.zip
/usr/lib/python3.10
/usr/lib/python3.10/lib-dynload
/home/burak/.local/lib/python3.10/site-packages
/usr/local/lib/python3.10/dist-packages
/usr/lib/python3/dist-packages
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 -c "import plotly; print(plotly.__version__)"
6.8.0
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 -c "import kaleido; print('kaleido ok')"
kaleido ok





burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ plotly_get_chrome

Plotly will install a copy of Google Chrome to be used for generating static images of plots.
Chrome will be installed at: None
Do you want to proceed? [y/n] y
Installing Chrome for Plotly...
Chrome installed successfully.
The Chrome executable is now located at: /home/burak/.local/share/choreographer/deps/chrome-linux64/chrome










burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 benchmark.py
Starting benchmark suite...
Databases: MySQL 8.0 | PostgreSQL 18 | SQLite 3.45
Scenarios: INSERT(1K/10K/100K) | SELECT | JOIN | AGGREGATION | UPDATE/DELETE
Runs per scenario: 5\n
\n=== Connection Overhead (5 measurements each) ===
  mysql         mean=   8.32ms  std=  1.26ms
  postgresql    mean=  15.69ms  std=  3.00ms
  sqlite        mean=   4.55ms  std=  2.08ms
\n=== MySQL ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  MySQL done ✓
\n=== PostgreSQL ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  PostgreSQL done ✓
\n=== SQLite ===
  bulk_insert_1000 ...
  bulk_insert_10000 ...
  bulk_insert_100000 ...
  select_where ...
  complex_join ...
  aggregation ...
  update_delete ...
  SQLite done ✓
\n================================================================================
DB             Scenario                Mean (ms)   Std (ms)   Runs
================================================================================
mysql          bulk_insert_1000           102.48      24.54      5
mysql          bulk_insert_10000          861.10      74.16      5
mysql          bulk_insert_100000        8388.94     708.61      5
mysql          select_where                 3.37       0.88      5
mysql          complex_join                11.74       9.68      5
mysql          aggregation               2592.40     262.41      5
mysql          update_delete              700.46      72.16      5
postgresql     bulk_insert_1000            72.53      46.65      5
postgresql     bulk_insert_10000          515.54      32.31      5
postgresql     bulk_insert_100000        4791.79     207.67      5
postgresql     select_where                 2.05       2.20      5
postgresql     complex_join                12.29       4.32      5
postgresql     aggregation                217.31      46.77      5
postgresql     update_delete              592.11     603.34      5
sqlite         bulk_insert_1000           180.51      11.56      5
sqlite         bulk_insert_10000          966.01      96.96      5
sqlite         bulk_insert_100000        3578.62     352.00      5
sqlite         select_where                71.44       8.30      5
sqlite         complex_join               506.45      27.57      5
sqlite         aggregation              93859.33    1734.00      5
sqlite         update_delete             8050.68    3510.72      5
================================================================================
\nResults saved to results.csv
\nDone! Run report.py to generate charts.
burak@DESKTOP-TDTDREU:/mnt/c/Users/Burak/Desktop/anul1master/pdd/project/proiect_pdd$ python3 report.py

======================================================================
DB             Scenario                   Mean (ms)   Std (ms)
======================================================================
mysql          bulk_insert_1000              102.48      24.54
mysql          bulk_insert_10000             861.10      74.16
mysql          bulk_insert_100000           8388.94     708.61
mysql          select_where                    3.37       0.89
mysql          complex_join                   11.74       9.68
mysql          aggregation                  2592.40     262.41
mysql          update_delete                 700.47      72.16
postgresql     bulk_insert_1000               72.53      46.65
postgresql     bulk_insert_10000             515.54      32.31
postgresql     bulk_insert_100000           4791.79     207.67
postgresql     select_where                    2.05       2.20
postgresql     complex_join                   12.29       4.32
postgresql     aggregation                   217.31      46.77
postgresql     update_delete                 592.11     603.34
sqlite         bulk_insert_1000              180.51      11.55
sqlite         bulk_insert_10000             966.01      96.96
sqlite         bulk_insert_100000           3578.62     352.00
sqlite         select_where                   71.44       8.30
sqlite         complex_join                  506.45      27.57
sqlite         aggregation                 93859.33    1734.00
sqlite         update_delete                8050.68    3510.72
======================================================================

Generating charts...
  Saved: chart_insert.png
  Saved: chart_query.png
  Saved: chart_update_delete.png
  Saved: chart_summary.png
  All charts saved.

Done!