import schematics

def valid_goal_expectation(value):
    if value < 0:
        raise schematics.exceptions.ValidationError(u'Must be a positive float')
    elif value > 15:
        raise schematics.exceptions.ValidationError(u'Expected goals must be <= 15')
    else:
        return value

class FootballRequest(schematics.Model):
    game_id = schematics.types.StringType(required=True)
    home_expected = schematics.types.FloatType(required=True, validators=[valid_goal_expectation])
    away_expected = schematics.types.FloatType(required=True, validators=[valid_goal_expectation])


class FootballResponse(schematics.Model):
    game_id = schematics.types.StringType(required=True)
    home = schematics.types.FloatType(required=True)
    away = schematics.types.FloatType(required=True)
    draw = schematics.types.FloatType(required=True)

