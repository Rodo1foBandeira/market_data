CREATE PROCEDURE export_active_by_date 
(IN active_ini VARCHAR(6), IN date_ymd VARCHAR(10))
BEGIN
	DECLARE out_file VARCHAR(100);
	SET out_file = CONCAT('/var/lib/mysql-files/market_data/', date_ymd, '_', active_ini, '.csv');
	SET @q1 = CONCAT('SELECT DATE_FORMAT(datetime_buss, "%T.%f") h_m_s_ms, buyer, seller, price, qtd, tot_qtd, tot_buss ',
	  'FROM mining_trade ',
	 'WHERE active like "', active_ini, '%" ',
	   "AND DATE_FORMAT(datetime_buss, '%Y-%m-%d') = '", date_ymd,
	"' INTO OUTFILE '", out_file, "' FIELDS TERMINATED BY ',' ENCLOSED BY '", '"', "' LINES TERMINATED BY '\n'");
	
	prepare s1 from @q1;
	execute s1;
	deallocate prepare s1;
END