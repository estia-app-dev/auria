from typing import List, Dict

from firebase_admin import auth
from firebase_admin.auth import UserRecord, DeleteUsersResult

from auria.utils.RandomUtils import RandomUtils


class FirebaseAuthApi:

  @staticmethod
  def createUser(uuid: str, email: str, password: str, emailVerified: bool = False, phoneNumber: str = None) -> UserRecord:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#create_user
    user = auth.create_user(
      uid=uuid,
      email=email,
      email_verified=emailVerified,
      phone_number=phoneNumber,
      password=password,
      disabled=False)
    return user

  @staticmethod
  def deleteUser(uid: str):
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#delete_user
    auth.delete_user(uid)

  @staticmethod
  def deleteUsers(uid: List[str]) -> DeleteUsersResult:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#delete_users
    return auth.delete_users(uid)

  @staticmethod
  def updateEmailAddress(uuid: str, email: str) -> UserRecord:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#update_user
    user = auth.update_user(
      uid=uuid,
      email=email,
      email_verified=False)
    return user

  @staticmethod
  def updateUserPassword(uuid: str, password: str) -> UserRecord:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#update_user
    user = auth.update_user(
      uid=uuid,
      password=password)
    return user

  @staticmethod
  def verifyIdToken(token: str) -> dict:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#verify_id_token
    return auth.verify_id_token(id_token=token, check_revoked=True)

  @staticmethod
  def getUserUidByEmail(email: str) -> UserRecord:
    # https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#get_user_by_email
    return auth.get_user_by_email(email)

  @staticmethod
  def createCustomToken(additionalClaims: Dict):
    uid = RandomUtils.uuid()
    additionalClaims['id'] = RandomUtils.uuid()  # Ne sert à rien, juste pour embrouiller celui qui lit le jwt

    return auth.create_custom_token(uid, additionalClaims)
