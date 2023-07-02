from typing import List

from firebase_admin import messaging
from firebase_admin.messaging import Message, MulticastMessage, BatchResponse, APNSConfig, ApsAlert

from auria.external_services.firebase.messaging.FirebaseMessage import FirebaseMessage, FirebaseMulticastMessage


class FirebaseMessagingApi:

  @staticmethod
  def _APNSConfig(body: str) -> APNSConfig:
    return APNSConfig(
        # headers={
        #   'apns-push-type': 'background',
        #   'apns-priority': '5'
        # },
        payload=messaging.APNSPayload(aps=messaging.Aps(
          alert=ApsAlert(body=body)
        ))
      )

  @staticmethod
  def send(message: FirebaseMessage) -> str:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging#send

    preparedMessage = Message(
      token=message.token,
      data=message.data,

      # SI ON ACTIVE CES LIGNES, LES NOTIFICATIONS EN BACKGROUND SUR ANDROID
      # NE SONT PLUS TRIGGER, ON JUSTE L'ALERTE SANS LES TRAITEMENTS REALM ET CIE
      # notification=messaging.Notification(
      #   body=self.request.body
      # ),
      apns=FirebaseMessagingApi._APNSConfig(message.body)
    )

    return messaging.send(message=preparedMessage,  dry_run=message.forTesting)

  @staticmethod
  def sendForAll(message: FirebaseMulticastMessage) -> BatchResponse:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.messaging#send

    preparedMessage = MulticastMessage(
      tokens=message.tokens,
      data=message.data,

      # SI ON ACTIVE CES LIGNES, LES NOTIFICATIONS EN BACKGROUND SUR ANDROID
      # NE SONT PLUS TRIGGER, ON JUSTE L'ALERTE SANS LES TRAITEMENTS REALM ET CIE
      # notification=messaging.Notification(
      #   body=self.request.body
      # ),
      apns=FirebaseMessagingApi._APNSConfig(message.body)
    )

    return messaging.send_each_for_multicast(multicast_message=preparedMessage, dry_run=message.forTesting)
