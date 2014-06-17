# encoding: utf-8
# vim: expandtab ts=2

from thoureport.messages.parser import *
from thousand.settings import THE_DATABASE
import psycopg2
import re

__DEFAULTS    = DATABASES['default']
THE_DATABASE  = psycopg2.connect(database = __DEFAULTS['NAME'],
                                     user = __DEFAULTS['USER'],
                                 password = __DEFAULTS['PASSWORD'],
                                     host = __DEFAULTS['HOST'])

# TODO:
# Load the report(s).
# Find a report.
class ThouReport:
  'The base class for all "RapidSMS 1000 Days" reports.'
  created   = False
  columned  = False

  def __init__(self, msg):
    'Initialised with the Message object to which it is coupled.'
    self.msg  = msg

  def __insertables(self, fds):
    '''Returns a hash of all the columns that will be affected by an insertion of this report into the database. The column name is the key, with its value.'''
    cvs   = {}
    ents  = self.msg.entries
    for fx in ents:
      curfd = ents[fx]
      if curfd.several_fields:
        for vl in curfd.working_value:
          cvs[('%s_%s' % (fx, vl)).lower()] = vl
      else:
        try:
          cvs[fx] = curfd.working_value[0]
        except IndexError:
          raise Exception, ('No value supplied for column \'%s\' (%s)' % (fx, str(curfd)))
    return cvs

  # TODO: Consider the message field classes' declared default.
  def save(self):
    '''This method saves the report object into the table for that report class, returning the index as an integer.
It is not idempotent at this level; further constraints should be added by inheriting classes.'''
    tbl, cols = self.msg.__class__.create_in_db(self.__class__)
    cvs       = self.__insertables(cols)
    curz      = THE_DATABASE.cursor()
    cpt       = []
    vpt       = []
    for coln, _, escer, _ in cols:
      if coln in cvs:
        cpt.append(coln)
        vpt.append(escer.dbvalue(cvs[coln], curz))
    qry = 'INSERT INTO %s (%s) VALUES (%s) RETURNING indexcol;' % (tbl, ', '.join(cpt), ', '.join(vpt)) 
    curz.execute(qry)
    ans = curz.fetchone()[0]
    curz.close()
    return ans

  @classmethod
  def describe(self, tn):
    if not cvs:
      if tn.__class__ == self:
        tn, cols = self.msg.__class__.creation_sql(self.__class__)
        return cols
      raise ValueError, 'describe wants a (string), a ([string]), or a (ThouReport).'
    if type(cvs) == type([]):
      return [self.describe(tn) for cv in cvs]
    tbl   = str(tn)
    ans   = []
    curz  = db.cursor()
    curz.execute('SELECT column_name FROM information_schema.columns WHERE table_name = %s', (tbl,))
    for rw in curz.fetchall():
      ans.append(rw[0])
    curz.close()
    return ans

  @classmethod
  def query(self, djconds, tn = None):
    if not tn: return self.query(djconds, __DEFAULTS['REPORTS'])
    cols  = self.describe(tn)
    qry   = 'SELECT %s FROM %s' % (', '.join(cols), tn)
    raise Exception, qry
    curz  = db.cursor()
    curz.execute(qry)
    ans   = curz.fetchall()
    curz.close()
    return (cols, ans)

  @classmethod
  def sparse_matrix(self, tn, cvs = None):
    if not cvs:
      if tn.__class__ == self:
        tn, cols = self.msg.__class__.creation_sql(self.__class__)
        return self.sparse_matrix(tn, self.__insertables(cols))
      raise ValueError, 'sparse_matrix wants a (string, hash), a (string, [hash]), or a (ThouReport).'
    if type(cvs) == type([]):
      return [self.sparse_matrix(tn, cv) for cv in cvs]
    if type(cvs) == type({}):
      return self.sparse_matrix_core(tn, cvs)
    raise Exception, ('What sparse matrix is %s?' % (str(cvs),))

  @classmethod
  def sparse_matrix_core(self, tn, hsh):
    try:
      tbl, cols = tn, hsh.keys()
      curz      = db.cursor()
      curz.execute('SELECT TRUE FROM information_schema.tables WHERE table_name = %s', (tbl,))
      if not curz.fetchone():
        curz.execute('CREATE TABLE %s (indexcol SERIAL NOT NULL, created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW());' % (tbl,))
        curz.close()
        return self.create_in_db(repc)
      for col in cols:
        colnm = '%s_%s' % (tbl, col[0])
        curz.execute('SELECT TRUE FROM information_schema.columns WHERE table_name = %s AND column_name = %s', (tbl, colnm))
        if not curz.fetchone():
          curz.execute('ALTER TABLE %s ADD COLUMN %s %s;' % (tbl, colnm, col[1]))
      curz.close()
      db.commit()
      self.created  = True
      return stuff
    except Exception, e:
      raise Exception, ('Table creation: ' + str(e))

  @classmethod
  def load(self, msgtxt):
    with ThouMessage.parse(msgtxt) as msg:
      return self(msg)

class ThouTable:
  def __init__(self, cols, rows = None):
    self.names  = cols
    self.__set_names()
    self.query  = rows

  def __set_names(self):
    dem         = self.names
    self.names  = {}
    notI        = 0
    for x in dem:
      self.names[x] = notI
      notI          = notI + 1

  def rows(self):
    return self.query

  def __getitem__(self, them):
    if type(them) != slice:
      raise ValueError, 'Should be a slice [column-name:row]'
    try:
      return them.stop[self.names[them.start]]
    except ValueError:
      raise NameError, ('No column called "%s" (has: %s).' % (colnm, ', '.join(cols)))
