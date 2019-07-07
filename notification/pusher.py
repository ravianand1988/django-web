from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='78db0b73-4c87-4dc5-8fd1-77a5fee93390',
    secret_key='AA13DF04AD1EEC4FDFA58871EBC72993D26EFED8B0654329F1C194C1F02BE5D2',
)


def send_push_notification(instance):
    response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={
            'fcm': {
                'notification': {
                    'title': instance.title,
                    'body': instance.message,
                },
            },
        },
    )

    print(response['publishId'])
