from flask import Flask,request, jsonify
from flask_restful import Resource, Api, fields, marshal_with,abort
import pymysql
from flask_cors import CORS


connection = pymysql.connect(
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="nayemuddin-mnubpial-project-1.h.aivencloud.com",
  password="AVNS_sftvfHF-LZN1CKvPJT1",
  port=18706,
  user="avnadmin",
)


cursor=connection.cursor()

app=Flask(__name__)

api=Api(app)

CORS(app)


field_serializer={
  'id':fields.Integer,
  'fullname':fields.String,
  'date_of_birth':fields.String,
  'gender':fields.String,
  'phone':fields.String,
  'address':fields.String,
  'email':fields.String,
  'username':fields.String,  
  'pass':fields.String
}


class users(Resource):
  # @marshal_with(field_serializer)
  # def get(self):
  #   cursor.execute('select * from user_info')
  #   return cursor.fetchall()

  @marshal_with(field_serializer)
  def post(self):
    data=request.json
    cursor.execute('select * from api_users where email=%s or username=%s',(data['email'],data['username']))
    if cursor.fetchone():
      abort(409,message='Data already exists')
    cursor.execute('insert into api_users '
    '(fullname,date_of_birth,gender,phone,address,email,username,pass) '
    'values(%s,%s,%s,%s,%s,%s,%s,%s)',
    (data['fullname'],data['date_of_birth'],data['gender'],data['phone'],data['address'],data['email'],data['username'],data['pass'],))
    connection.commit()
    # cursor.execute('select * from user_table')
    # return cursor.fetchall()
  
  
    # cursor.execute('select * from user_info')
    # return cursor.fetchall()



class user(Resource):
  @marshal_with(field_serializer)
  def post(self,user_mail):
    cursor.execute('select * from api_users where email=%s',(user_mail,))
    res=cursor.fetchone()
    if not res:
      abort(404,message="Data doesn't exist")
    return res

  @marshal_with(field_serializer)
  def patch(self,user_mail):
    data=request.json
    if len(data)>1:
      abort(400,message='Only one field allowed')
    elif 'email' in data:
      cursor.execute('update api_users set email=%s where email=%s',(data['email'],user_mail,))
    elif 'fullname' in data:
      cursor.execute('update api_users set fullname=%s where email=%s',(data['fullname'],user_mail,))
    elif 'pass' in data:
      cursor.execute('update api_users set pass=%s where email=%s',(data['pass'],user_mail,))
    connection.commit()
    # cursor.execute('select * from user_info where email=%s',(user_mail,))
    # return cursor.fetchone()

  @marshal_with(field_serializer)
  def put(self,user_mail):
    data=request.json
    if len(data)<3:
      abort(400,message='All fields required')
    cursor.execute(
      'update api_users '
      'set email=%s,fullname=%s,pass=%s '
      'where id=%s',(data['email'],data['fullname'],data['pass'],user_mail,)
    )
    connection.commit()
    # cursor.execute('select * from user_info where id=%s',(user_mail,))
    # return cursor.fetchone()

  @marshal_with(field_serializer)
  def delete(self,user_mail):
    cursor.execute("select id from api_users where email=%s",(user_mail,))
    user_id=cursor.fetchone()
    cursor.execute("delete from api_users where email=%s",(user_mail,))
    cursor.execute("update api_users set id=id-1 where id>%s",(user_id,))
    connection.commit()




api.add_resource(users,'/users')
api.add_resource(user,'/users/<string:user_mail>')



if __name__=='__main__':
  app.run(debug=True)