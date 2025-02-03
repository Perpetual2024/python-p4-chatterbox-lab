from datetime import datetime

from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        m = Message.query.filter(
            Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")

        for message in m:
            db.session.delete(message)

        db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():

            app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():

            response = app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            assert(response.content_type == 'application/json')

            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()


    def test_updates_body_of_message_in_database(self):
      '''updates the body of a message in the database.'''
      with app.app_context():

        # Ensure there's at least one message to update
        m = Message.query.first()
        if not m:
            # If the database is empty, create a message
            m = Message(body="Initial message", username="test_user")
            db.session.add(m)
            db.session.commit()

        id = m.id
        body = m.body

        # Perform the update
        app.test_client().patch(
            f'/messages/{id}',
            json={"body": "Goodbye 👋"}
        )

        # Check if the message was updated
        g = Message.query.get(id)  # Use .get(id) to directly fetch by primary key
        assert(g)
        assert(g.body == "Goodbye 👋")  # Ensure the body was updated

        # Revert the body to its original state
        g.body = body
        db.session.add(g)
        db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
      '''returns data for the updated message as JSON.'''
      with app.app_context():

        # Ensure there's at least one message to update
        m = Message.query.first()
        if not m:
            # If the database is empty, create a message
            m = Message(body="Initial message", username="test_user")
            db.session.add(m)
            db.session.commit()

        id = m.id

        # Perform the update
        response = app.test_client().patch(
            f'/messages/{id}',
            json={"body": "Goodbye 👋"}
        )

        # Assert response is correct
        assert(response.content_type == 'application/json')
        assert(response.json["body"] == "Goodbye 👋")

        # Fetch the updated message and assert its body is updated
        g = Message.query.get(id)
        assert(g.body == "Goodbye 👋")

        # Revert the body to its original state
        g.body = m.body
        db.session.add(g)
        db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)