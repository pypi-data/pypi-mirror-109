from localstack.utils.aws import aws_models
Wnxmk=super
Wnxmy=None
Wnxmz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Wnxmk(LambdaLayer,self).__init__(arn)
  self.cwd=Wnxmy
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Wnxmz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(RDSDatabase,self).__init__(Wnxmz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(RDSCluster,self).__init__(Wnxmz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(AppSyncAPI,self).__init__(Wnxmz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(AmplifyApp,self).__init__(Wnxmz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(ElastiCacheCluster,self).__init__(Wnxmz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(TransferServer,self).__init__(Wnxmz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(CloudFrontDistribution,self).__init__(Wnxmz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Wnxmz,env=Wnxmy):
  Wnxmk(CodeCommitRepository,self).__init__(Wnxmz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
