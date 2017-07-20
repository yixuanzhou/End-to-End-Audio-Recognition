#!/usr/bin/python  
#-*- coding:utf-8 -*-  
from thrift import Thrift
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase

import struct
# Method for encoding ints with Thrift's string encoding
def encode(n):
   return struct.pack("i", n)

# Method for decoding ints with Thrift's string encoding
def decode(s):
   return int(s) if s.isdigit() else struct.unpack('i', s)[0]


class HBaseAji(object):

   def __init__(self, table='audio2text', host='127.0.0.1', port=9090):
       #hdp.ajmide.net:8080
       self.table = table
       self.host = host
       self.port = port

       # Connect to HBase Thrift server
       self.transport = TTransport.TBufferedTransport(TSocket.TSocket(host, port))
       self.protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)
       
       # Create and open the client connection
       self.client = Hbase.Client(self.protocol)
       self.transport.open()

       # set type and field of column families
       self.set_column_families([int, str, str], ['type', 'typename', 'content'])
       #self.set_column_families([str, str, int], ['name', 'sex', 'age'])
       self._build_column_families()

   def set_column_families(self, type_list, col_list):
       self.columnFamiliesType = type_list
       self.columnFamilies = col_list

   def _build_column_families(self):
       """ give all column families name list, create a table
       """
       tables = self.client.getTableNames()
       if self.table not in tables:
           self.__create_table(self.table)

   def __create_table(self, table):
       """ create table in hbase with column families
       """
       columnFamilies = []
       for columnFamily in self.columnFamilies:
           name = Hbase.ColumnDescriptor(name=columnFamily)
           columnFamilies.append(name)
       self.client.createTable(table, columnFamilies)

   def __del__(self):
       self.transport.close()

   def __del_table(self, table):
       """ Delete a table, first need to disable it.
       """
       self.client.disableTable(table)
       self.client.deleteTable(table)

   def getColumnDescriptors(self):
       return self.client.getColumnDescriptors(self.table)

   def put(self, rowKey, qualifier='0', *args):
       """ put one row

       :param *args: all values correspond to column families.
           e.g. [name, sex, age]

       Usage::

       >>> HBaseTest().put('test', '0', 'john', 'male', '95')

       """
       mutations = []
       for j, column in enumerate(args):
           if isinstance(column, str):
               m_name = Hbase.Mutation(column=self.columnFamilies[j]+':'+qualifier, value=column)
           elif isinstance(column, int):
               m_name = Hbase.Mutation(column=self.columnFamilies[j]+':'+qualifier, value=encode(column))
           mutations.append(m_name)
       self.client.mutateRow(self.table, rowKey, mutations, {})

   def puts(self, rowKeys, values, qualifier='1'):
       """ put sevel rows, `qualifier` is autoincrement

       :param rowKeys: a single rowKey
       :param values: values is a 2-dimension list, one piece element is [name, sex, age]
       :param qualifier: column family qualifier

       Usage::

       >>> HBaseTest().puts('test', [['lee', 'f', '27'], ['clark', 'm', 27], ['dan', 'f', '27']])

       """
       mutationsBatch = []
       if not isinstance(rowKeys, list):
           rowKeys = [rowKeys] * len(values)

       for i, value in enumerate(values):
           mutations = []
           for j, column in enumerate(value):
               if isinstance(column, str):
                   m_name = Hbase.Mutation(column=self.columnFamilies[j]+':'+qualifier, value=column)
               elif isinstance(column, int):
                   m_name = Hbase.Mutation(column=self.columnFamilies[j]+':'+qualifier, value=encode(column))
               mutations.append(m_name)

           qualifier = str( int(qualifier) + 1 )
           mutationsBatch.append( Hbase.BatchMutation(row=rowKeys[i], mutations=mutations) )
       self.client.mutateRows(self.table, mutationsBatch, {})


   def getRow(self, row, qualifier='0'):
       """ get one row from hbase table

       :param row: row key
       """
       rows = self.client.getRow(self.table, row, {})
       ret = []
       for r in rows:
           rd = { 'row': r.row }
           for j, column in enumerate(self.columnFamilies):
               if self.columnFamiliesType[j] == str:
                   rd.update({ column: r.columns.get(column+':'+qualifier).value })
               elif self.columnFamiliesType[j] == int:
                   rd.update({ column: decode(r.columns.get(column+':'+qualifier).value) })
           ret.append(rd)
       return ret

   def getRows(self, rows, qualifier='0'):
       """ get rows from hbase table, all the row specify the same `qualifier`

       :param rows: a list of row key
       """
       grow = True if len(set(rows)) == 1 else False

       for r in rows:
           yield self.getRow(r, qualifier)
           if grow: qualifier = str( int(qualifier) + 1 )


   def scanner(self, numRows=100, startRow=None, stopRow=None):
       """ scan the table

       :param numRows: how much rows return in one iteration.
       :param startRow: start scan row key
       :param stopRow: stop scan row key
       """
       scan = Hbase.TScan(startRow, stopRow)
       scannerId = self.client.scannerOpenWithScan(self.table, scan, {})
       #row = self.client.scannerGet(scannerId)

       ret = []
       rowList = self.client.scannerGetList(scannerId, numRows)
       while rowList:
           for r in rowList:
               rd = { 'row': r.row }
               for k, v in r.columns.iteritems():
                   cf, qualifier = k.split(':')
                   if qualifier not in rd:
                       rd[qualifier] = {}

                   idx = self.columnFamilies.index(cf)
                   if self.columnFamiliesType[idx] == str:
                       rd[qualifier].update({ cf: v.value })
                   elif self.columnFamiliesType[idx] == int:
                       rd[qualifier].update({ cf: decode(v.value) })

               ret.append(rd)
           
           rowList = self.client.scannerGetList(scannerId, numRows)

       self.client.scannerClose(scannerId)
       return ret

   def scanWithKeyword(self, __filter):
       scan = Hbase.TScan()
       #print "ValueFilter(=,'substring:%s')" %(__filter)
       scan.columns = ['content:0']
       scan.filterString = "ValueFilter(=,'substring:%s')" %(__filter)
       scannerId = self.client.scannerOpenWithScan(self.table, scan, {})
       result = self.client.scannerGetList(scannerId, 100)
       return result

def demo():
   ht = HBaseAji(table='1test1')
   values = [['lee', 'f', 27], ['clark', 'm', 27], ['dan', 'f', 27]]
   rowKey = 'cookie'
   ht.put(rowKey, 'fish', 'f', '22')
   ht.puts(rowKey, values)
   #print ht.getColumnDescriptors()

   #print ht.getRow(rowKey)
   for i in ht.getRows([rowKey] * 4):
       print(i)
   #print ht.scanner()

if __name__ == '__main__':
   #demo()
   pass
   