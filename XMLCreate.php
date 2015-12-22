<?php
mysql_connect('10.0.0.14', 'monitor', 'raspberry');
mysql_select_db('Monitor');

$sql = "SELECT * FROM Monitor.Server;";
$res = mysql_query($sql);

$xml = new XMLWriter();

$xml->openURI("php://output");
$xml->startDocument();
$xml->setIndent(true);

$xml->startElement('data');
$xml->startElement('servers');
while ($row = mysql_fetch_assoc($res)) {
  $xml->startElement("server");

//  $xml->writeAttribute('name', $row['udid']);
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

header('Content-type: text/xml');
$xml->flush();
?>