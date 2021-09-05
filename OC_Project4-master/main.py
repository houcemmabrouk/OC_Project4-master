from views.view import View
from controllers.controller import Controller


def main():
    view = View()
    projet = Controller(view)
    projet.run()

if __name__ == '__main__':
    main()