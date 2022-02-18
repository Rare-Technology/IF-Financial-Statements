from ourfish.models import AuthUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class OurfishAuthBackend:
    def authenticate(self, request, username, password):
        """
        Custom authentication backend to handle Ourfish authentication information.
        This is likely a temporary solution, but the idea is:
        If the user exists in User and the password is correct, return that.
        Otherwise, find the user in AuthUser and create a new User with the AuthUser info. Return the new User user.
        If password validation fails at any point or if the user DNE in AuthUser, return None
        One problem that could happen is if a user in AuthUser is deleted, that will not propagate to User.

        But for the mean time this solves the problem of reading user information from Ourfish without
        modifying the Ourfish table, and using a User model that has expected User methods (AuthUser, as is
        currently implemented, does not have methods like authenticate or check_password).
        """
        try:
            user = User.objects.get(username = username)
            valid_pass = check_password(password, user.password)

            if valid_pass:
                return user

        except User.DoesNotExist:
            try:
                of_user = AuthUser.objects.get(username = username)
                of_valid_pass = check_password(password, of_user.password)

                if of_valid_pass:
                    new_user = User(
                        username = of_user.username,
                        password = of_user.password,
                        email = of_user.email,
                        first_name = of_user.first_name,
                        last_name = of_user.last_name,
                        date_joined = of_user.date_joined,
                        last_login = of_user.last_login,
                        is_active = of_user.is_active,
                        is_staff = of_user.is_staff,
                        is_superuser = of_user.is_superuser
                    )
                    new_user.save()
                    return new_user

            except AuthUser.DoesNotExist:
                pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
                return None
