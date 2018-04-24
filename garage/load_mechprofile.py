import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "garage.settings")

import django
django.setup()

from accounts.models import MechProfile


def save_mechprofile_from_row(mechprofile_row):
    mechprofile = MechProfile()
    mechprofile.id = mechprofile_row[0]
    mechprofile.owner = mechprofile_row[1]
    mechprofile.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print ("Reading from file " + str(sys.argv[1]))
        mechprofile_df = pd.read_csv(sys.argv[1])
        print( mechprofile_df)

        mechprofile_df.apply(
            save_mechprofile_from_row,
            axis=1
        )

        print ("There are {} mechprofile".format(MechProfile.objects.count()))

    else:
        print ("Please, provide Wine file path")
