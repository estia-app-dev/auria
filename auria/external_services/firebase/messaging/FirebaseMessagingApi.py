from firebase_admin import messaging
from firebase_admin.messaging import Message, APNSConfig, ApsAlert

from auria.external_services.firebase.messaging.FCMMessage import FCMMessage


class FirebaseMessagingApi:

  @staticmethod
  def send(message: FCMMessage, forTesting=False) -> str:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging#send

    preparedMessage = Message(
      token=message.token,
      data=message.data,

      # SI ON ACTIVE CES LIGNES, LES NOTIFICATIONS EN BACKGROUND SUR ANDROID
      # NE SONT PLUS TRIGGER, ON JUSTE L'ALERTE SANS LES TRAITEMENTS REALM ET CIE
      # notification=messaging.Notification(
      #   body=self.request.body
      # ),
      apns=APNSConfig(
        # headers={
        #   'apns-push-type': 'background',
        #   'apns-priority': '5'
        # },
        payload=messaging.APNSPayload(aps=messaging.Aps(
          alert=ApsAlert(body=message.text)
        ))
      )
    )

    return messaging.send(message=preparedMessage, dry_run=forTesting)
