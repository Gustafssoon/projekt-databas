from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup


class PlayerAdmin(ModelView):
    column_list = (
        "headshot_url",
        "player_id",
        "first_name",
        "last_name",
        "primary_position",
    )

    column_labels = {
        "headshot_url": "Foto"
    }

    column_formatters = {
        "headshot_url": lambda v, c, m, p: Markup(
            f'''
            <div style="text-align:center;">
                <img src="{m.headshot_url}" 
                    style="width:40px;height:40px;border-radius:50%;object-fit:cover;">
            </div>
            '''
        ) if m.headshot_url else ""
    }
