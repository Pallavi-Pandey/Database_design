```
Table message{
  message_id integer [primary key]
  from_number integer
  to_number integer
  message_text text
  send_datetime timestamp
  conversation_id integer 
}

Table contact{
  contact_id integer [primary key]
  first_name varchar
  last_name varchar
  profile_photo image
  phone_no integer
}

Table group_member{
  contact_id integer
  conversation_id integer
  joined_date timestamp
  left_date timestamp
}

Table conversation{
  conversation_id integer [primary key]
  conversation_name varchar
}

Ref: message.conversation_id > conversation.conversation_id

Ref: contact.contact_id > group_member.contact_id

Ref: conversation.conversation_id > group_member.conversation_id
```
![alt text](image.png)