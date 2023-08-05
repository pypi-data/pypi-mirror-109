from sdsRayanArvin.Api import Api
from sdsRayanArvin.Request import Request


class Factory:
    """python samacontrol architecture"""

    def __init__(self, api='Old', Url=None):
        print('create instance and config api: ' + api)
        self.RequestApi = None
        self.apiName = None
        self.__ApiConnected = self.__API(api, Url)

    def __API(self, api='Old', Url=None):
        if self.RequestApi is not None:
            return self.RequestApi

        if api == 'Old':
            request = Request('https://samacontrol.ir/sama/api/')

        if api == 'Data':
            request = Request('https://samacontrol.ir/device_data_managment/')

        if api == 'Workflow':
            request = Request('https://samacontrol.ir/workflow-service/')

        if api == 'Rule':
            request = Request('https://samacontrol.ir/rule-service/')

        if api == 'Weather':
            request = Request('https://samacontrol.ir/weather/')

        if api == 'RuleExe':
            request = Request('https://samacontrol.ir/rule-exe/')

        if api == 'WorkflowsExe':
            request = Request('https://samacontrol.ir/workflow-exe/')

        if api == 'Log':
            request = Request('http://49a79b8b-022f-487a-86f6-dfb43132b8b0.hsvc.ir:30122/')

        self.apiName = api
        self.RequestApi = request

        # connect to API
        return self.__connectToApi()

    def __connectToApi(self):
        if self.RequestApi is None:
            print('please set API then connect to API.')

        return Api(self.RequestApi)

    def connectToRepo(self, repository):
        return self.__ApiConnected.instanceOfRepository(repository)


# user = Factory()
# authenticate = user.connectToRepo(Authenticate)
# authenticate.Login()

# rule = Factory('Rule')
# rule.RequestApi.setToken(user.RequestApi.getToken())
# aux: Rule = rule.connectToRepo(Rule)
# aux.allRule()

# aux: AuxStation = user.connectToRepo(AuxStation)
# aux.AuxOnID('294')
# aux.AuxOnID('294')
# sleep(15)
# aux.AuxOnID('294')
#
# data = Factory('Data')
# data.RequestApi.setToken(user.RequestApi.getToken())
# lastData: Data = data.connectToRepo(Data)
# lastData.StoreDataOnTopic({
#     'topic': 1,
#     'type': 'DO',
#     'data': '1',
#     'pan': 0,
#     'add': 0,
# })
# x = lastData.LastDataOnTopic('866600042708784', 'DO', '0', '0')
# print(x.getType())
# x = authenticate.UserInformation()

#
# obj: Object = user.connectToRepo(Object)
# obj.ObjectByIdOrg()
# print(obj.ObjectByIdOrg()[0].getTitle())

# workflow = Factory('Workflow')
# workflow.RequestApi.setToken(user.RequestApi.getToken())
# lastData = workflow.connectToRepo(Workflows)
# lastData.dataAll()

# log = Factory('LogApi')
# logwp: LogApi = log.connectToRepo(LogApi)
# logwp.WorkflowLog('1367', '0', '17')
