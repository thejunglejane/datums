from datums import models


def human_to_boolean(human):
    if not isinstance(human, list) or len(human) == 0:
        return None
    if human[0].lower() == 'yes':
        return True
    return False

token_accessor = models.base.ResponseClassLegacyAccessor(
    models.TokenResponse, 'tokens_response',
    (lambda x: [i['text'] for i in x.get('tokens', [])]))

multi_accessor = models.base.ResponseClassLegacyAccessor(
    models.MultiResponse, 'multi_response',
    (lambda x: x.get('answeredOptions')))

boolean_accessor = models.base.ResponseClassLegacyAccessor(
    models.BooleanResponse, 'boolean_response',
    (lambda x: human_to_boolean(x.get('answeredOptions'))))

location_accessor = models.base.LocationResponseClassLegacyAccessor(
    models.LocationResponse, 'location_response',
    (lambda x: x['locationResponse'].get(
        'text') if x.get('locationResponse') else None),
    'venue_id', (lambda x: x['locationResponse'].get(
        'foursquareVenueId') if x.get('locationResponse') else None))

people_accessor = models.base.ResponseClassLegacyAccessor(
    models.PeopleResponse, 'people_response',
    (lambda x: [i['text'] for i in x.get('tokens', [])]))

numeric_accessor = models.base.ResponseClassLegacyAccessor(
    models.NumericResponse, 'numeric_response',
    (lambda x: float(
        x.get('numericResponse')) if bool(x.get('numericResponse')) else None))

note_accessor = models.base.ResponseClassLegacyAccessor(
    models.NoteResponse, 'note_response',
    (lambda x: [i.get('text') for i in x.get('textResponses', [])]))


def get_response_accessor(response, snapshot):
    # Determine the question ID and response type based on the prompt
    question_id, response_type = models.session.query(
        models.Question.id, models.Question.type).filter(
            models.Question.prompt == response['questionPrompt']).first()

    ids = {'question_id': question_id,  # set the question ID
           'snapshot_id': snapshot['uniqueIdentifier']}  # set the snapshot ID

    # Dictionary mapping response type to response class, column, and accessor
    # mapper
    response_mapper = {0: token_accessor, 1: multi_accessor,
                       2: boolean_accessor, 3: location_accessor,
                       4: people_accessor, 5: numeric_accessor,
                       6: note_accessor}

    return response_mapper[response_type], ids
