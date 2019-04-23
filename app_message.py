import argparse
from models.connect_with_db import get_connection
from models import User, Message

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='LOGIN', required=False, action='store')
parser.add_argument('-p', '--password', help='PASSWORD', required=False, action='store')
parser.add_argument('-l', '--list', help='LIST MESSAGES', required=False, action='store_true', default=False)
parser.add_argument('-t', '--to', help='USER TO SEND', required=False, action='store')
parser.add_argument('-s', '--send', help='SEND', required=False, action='store')

args = parser.parse_args()

# """LISTS ALL MESSAGES TO THIS USER"""
if args.username is not None \
    and args.password is not None \
    and args.list is True \
    and args.to is None \
    and args.send is None:
    connection = get_connection()
    cursor = connection.cursor()
    user = User.load_user_by_username(cursor, args.username)
    if user is False:
        print(f'USER {args.username} DOES NOT EXIST')
    elif user.check_password(args.password) is True:
        message = Message.load_all_messages_to_user(user.id, cursor)
        if len(message) == 0:
            print(f'USER {args.username} DOES NOT RECEIVE ANY MESSAGE')
        else:
            print(f'MESSAGES TO USER {args.username}')
            for item in message:
                print(item.text)

    else:
        print('WRONG PASSWORD')

# """SENDING MESSAGES"""
elif args.username is not None \
    and args.password is not None \
    and args.list is False \
    and args.to is not None \
    and args.send is not None:
    connection = get_connection()
    cursor = connection.cursor()
    user = User.load_user_by_username(cursor, args.username)
    to_user = User.load_user_by_id(cursor, args.to)
    if user is False:
        print(f'USER {args.username} DOES NOT EXIST')
    elif user.check_password(args.password) is False:
        print('WRONG PASSWORD')
    elif to_user is False:
        print('RECIPIENT DOES NOT EXIST')
    else:
        Message(user.id, args.to, args.send).save_to_db(cursor)
        print('MESSAGE HAS BEEN SEND')

else:
    print("WRONG ARGUMENTS")
    parser.print_help()
