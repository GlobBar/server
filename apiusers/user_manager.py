class UserManager():

    def createCustomAccessToken(self, pw_length):
        # GENERATE access token
        import random
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        acctoken = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            acctoken = acctoken + alphabet[next_index]
        return acctoken
