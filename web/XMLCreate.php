<?php
mysql_connect('10.0.0.30', 'monitor', 'raspberry');
mysql_select_db('Monitor');

$sql = "SELECT * FROM Monitor.server;";
$res = mysql_query($sql);

$xml = new XMLWriter();

$xml->openURI("php://output");
$xml->startDocument();
$xml->setIndent(true);

$xml->startElement('data');
	$xml->startElement('servers');
	while ($row = mysql_fetch_assoc($res)) {
		$xml->startElement("server");
			$xml->writeAttribute('name', $row['Name']);
			
			$xml->startElement("sID");
				$xml->writeRaw($row['sID']);
			$xml->endElement();
			
			$xml->startElement("IPAdres");
				$xml->writeRaw($row['IPAdres']);
			$xml->endElement();
			
			$xml->startElement("IPPort");
				$xml->writeRaw($row['IPPort']);
			$xml->endElement();
	  
		$xml->endElement();
	}
	$xml->endElement();

	$xml->startElement('database');
		$xml->startElement("dbIPAdres");
			$xml->writeRaw('10.0.0.14');
		$xml->endElement();
		
		$xml->startElement("dbUser");
			$xml->writeRaw('monitor');
		$xml->endElement();
		
		$xml->startElement("dbPassword");
			$xml->writeRaw('raspberry');
		$xml->endElement();
		
		$xml->startElement("dbDatabase");
			$xml->writeRaw('Monitor');
		$xml->endElement();
	  
	$xml->endElement();
$xml->endElement();

header('Content-type: text/xml');
$xml->flush();
?>