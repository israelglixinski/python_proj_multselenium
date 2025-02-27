CREATE TABLE passos (
	id_reg 		INTEGER PRIMARY KEY AUTOINCREMENT,
	dtm_insert 	DATETIME DEFAULT current_timestamp,
	rotina 		INTEGER,
	estagio		TEXT,
	ordem 		INTEGER,
	acao 		TEXT,
	ativo 		INTEGER,
	var_dict 	TEXT,
	sub_passos 	TEXT,
	descricao 	TEXT
	);

CREATE TABLE lotes (
	id_reg 			INTEGER PRIMARY KEY AUTOINCREMENT,
	dtm_insert 		DATETIME DEFAULT current_timestamp,
	rotina 			INTEGER,
	lote 			INTEGER,
	status_desc		TEXT,
	status_usrhost 	TEXT,
	status_dtm 		DATETIME,
	identificador 	TEXT,
	var_dict 		TEXT
	);	

CREATE TABLE configs_main (
	id_reg 			INTEGER PRIMARY KEY AUTOINCREMENT,
	ativo 			INTEGER,
	rotina 			INTEGER,
	lote 			INTEGER,
	max_qt_lote		INTEGER,
	delay 			INTEGER,
	horarios_exec	INTEGER,	
	sleep_time		INTEGER,
	api_porta		INTEGER,
	webdrivers		TEXT
	);


CREATE TABLE configs_usrhost (
	id_reg 			INTEGER PRIMARY KEY AUTOINCREMENT,
	dtm_insert 		DATETIME DEFAULT current_timestamp,
	rotina 			INTEGER,
	lote 			INTEGER,
	max_qt_lote		INTEGER,
	delay 			INTEGER,
	horarios_exec	INTEGER,	
	sleep_time		INTEGER,
	usr_host		TEXT,
	ativo 			INTEGER
	);

CREATE TABLE horarios_exec (
	id_reg 			INTEGER PRIMARY KEY AUTOINCREMENT,
	id_config		INTEGER,
	dia_semana		TEXT,
	horario_ini		TEXT,
	horario_fin		TEXT,
	excluir1_ini	TEXT,
	excluir1_fin	TEXT,
	excluir2_ini	TEXT,
	excluir2_fin	TEXT,
	excluir3_ini	TEXT,
	excluir3_fin	TEXT
	);

CREATE TABLE comandos (
	id_reg 			INTEGER PRIMARY KEY AUTOINCREMENT,
	dtm_insert 		DATETIME DEFAULT current_timestamp,
	id_config		INTEGER,
	usr_host		TEXT,
	ativo 			INTEGER,
	acao 			TEXT,
	variavel1 		TEXT,
	variavel2 		TEXT,
	variavel3 		TEXT,
	variavel4 		TEXT,
	variavel5 		TEXT
	);









