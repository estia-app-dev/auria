from auria.utils.SubProcessUtils import SubProcessUtils


class DatabaseCommand:

  def __init__(self, dbname: str, dbusername: str):
    self.dbname = dbname
    self.dbusername = dbusername

  def createDb(self):
    return SubProcessUtils.executeAndWait([
      'mysql',
      '-u', self.dbusername,
      '-e', 'CREATE DATABASE IF NOT EXISTS ' + self.dbname
    ])

  def dropDb(self):
    return SubProcessUtils.executeAndWait([
      'mysql',
      '-u', self.dbusername,
      '-e', 'DROP DATABASE IF EXISTS ' + self.dbname
    ])

  def exportData(self, outputFilePath: str):
    return SubProcessUtils.executeAndWait([
      'mysqldump',
      '--no-create-info',
      '--skip-comments',
      '-u', self.dbusername,
      self.dbname,
      '>', outputFilePath
    ])

  def exportStructure(self, outputFilePath: str):
    return SubProcessUtils.executeAndWait([
      'mysqldump',
      '-d',
      '--skip-comments',
      '-u', self.dbusername,
      self.dbname,
      '>', outputFilePath
    ])

  def importFile(self, filePath: str):
    return SubProcessUtils.executeAndWait([
      'mysql',
      '-u', self.dbusername,
      self.dbname,
      '<', filePath
    ])
