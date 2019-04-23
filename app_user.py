import argparse
from models.connect_with_db import get_connection
from models import User

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='LOGIN', required=False, action='store')
parser.add_argument('-p', '--password', help='PASSWORD', required=False, action='store')
parser.add_argument('-n', '--new_pass', help='NEW PASSWORD', required=False, action='store')
parser.add_argument('-l', '--list', help='LIST USERS', required=False, action='store_true', default=False)
parser.add_argument('-d', '--delete', help='DELETE', required=False, action='store_true', default=False)
parser.add_argument('-e', '--edit', help='EDIT', required=False, action='store_true', default=False)
parser.add_argument('-t', '--to', help='WHO DO YOU WANT TO SEND AN EMAIL', required=False, action='store')

args = parser.parse_args()

# """ADDING NEW USER"""
if args.username is not None \
    and args.password is not None \
    and args.new_pass is None\
    and args.list is False \
    and args.delete is False \
    and args.edit is False:
    if len(args.password) < 8:
        print('PASSWORD TOO SHORT')
    else:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            user = User(f'{args.username}', f"{args.username}@email.com")
            user.set_password(f'{args.password}')
            user.save_to_database(cursor)
            print('Stworzylem użytkownika')
        except Exception:
           print("USER ALREADY EXISTS")

# """CHANGE PASSWORD"""
elif args.username is not None \
    and args.password is not None \
    and args.edit is True \
    and args.new_pass is not None \
    and len(args.new_pass) > 8 \
    and args.list is False \
    and args.delete is False:
    connection = get_connection()
    cursor = connection.cursor()
    user = User.load_user_by_username(cursor, f'{args.username}')
    if user.check_password(args.password) is True:
        user.set_password(args.new_pass)
        print('PASSWORD CHANGED')
        user.save_to_database(cursor)
    else:
        print('WRONG OLD PASSWORD')

# """DELETED USER"""
elif args.username is not None \
    and args.password is not None \
    and args.delete is True \
    and args.new_pass is None \
    and args.edit is False \
    and args.list is False:
    connection = get_connection()
    cursor = connection.cursor()
    user = User.load_user_by_username(cursor, f'{args.username}')
    if User.load_user_by_username(cursor, f'{args.username}') is False:
        parser.error(f"USER {args.username} DOES NOT EXIST")
    elif user.check_password(args.password) is True:
        user.delete(cursor)
        print('USER HAS BEEN DELETED')
    else:
        print("WRONG PASSWORD")

# """LIST ALL USERS"""
elif args.list is True \
    and args.username is None \
    and args.password is None \
    and args.delete is False \
    and args.new_pass is None \
    and args.edit is False \
    and args.delete is False:
    connection = get_connection()
    cursor = connection.cursor()
    tab = User.load_all_user(cursor)
    for item in range(len(tab)):
        print(tab[item].id, tab[item].username, tab[item].email)

else:
    print("WRONG ARGUMENTS")
    parser.print_help()
