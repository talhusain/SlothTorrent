class AdminView(object):
    def show_page(self):
        print('--Admin View--')

class UserView(object):
    def show_page(self):
        print('--User View--')

class Dispatcher(object):
    def __init__(self):
        self.admin_view = AdminView()
        self.user_view = UserView()

    def dispatch(self, request):
        if request.type == Request.admin_type:
            self.admin_view.show_page()
        elif request.type == Request.user_type:
            self.user_view.show_page()
        else:
            print('Error')


class RequestController(object):
    def __init__(self):
        self.dispatcher = Dispatcher()

    def dispatch_request(self, request):
        if isinstance(request, Request):
            self.dispatcher.dispatch(request)
        else:
            print('Error')

class Request(object):
    admin_type = 'admin'
    user_type = 'user'

    def __init__(self, request):
        self.type = None
        request = request.lower()
        if request == self.admin_type:
            self.type = self.admin_type
        elif request == self.user_type:
            self.type = self.user_type

if __name__ == '__main__':
    front_controller = RequestController()
    front_controller.dispatch_request(Request('admin'))
    front_controller.dispatch_request(Request('user'))
    front_controller.dispatch_request(Request('empty'))
    front_controller.dispatch_request('empty')
