# -*- coding: utf-8 -*-


import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_supported_interfaces, get_slot, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces     
from ask_sdk_core.utils.viewport import get_viewport_profile
from ask_sdk_model.ui import SimpleCard,StandardCard, Image
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective as APLRenderDocumentDirective
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective as APLARenderDocumentDirective
from ask_sdk_model.interfaces.alexa.presentation.apl import (SetValueCommand, ExecuteCommandsDirective)
import json
from random import randrange
from shared import datasources2, test_speach_data, noise_data, teamsdatasource
from linechartdata import linedata
from ask_sdk_core.api_client import DefaultApiClient
import boto3

s3 = boto3.client("s3")
sb = SkillBuilder()
radioButtonText = "default"
bucket = "bpltables"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TOKEN = "buttontoken"
TICK_WIDTH = 3.0

''' 
create an emit the actual speach plus background sound.
for now just a placeholder the echos its arguments, the real version would have business logic
'''
def say_stats(handler_input, text_to_speak): 
        noise_index = randrange(0, 3)
        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_should_end_session(False)          
                .add_directive( 
                  APLARenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_with_data_sources"
                    },
                    datasources = {
                        "text": {
                          "speak": text_to_speak
                        },
                        "crowd": {
                            "noise": noise_data[noise_index][0],
                            "start": str(randrange(0, noise_data[noise_index][1]))
                        }
                        
                    }              
                  )
                ).response)


''' Returns the screen to the main page '''
def go_home(handler_input):
    return (
        handler_input.response_builder
            .speak("Welcome to Premier League")
            .set_should_end_session(False)          
            .add_directive( 
              APLRenderDocumentDirective(
                token= "developer-provided-string",
                document = {
                    "type" : "Link",
                    "token" : "my token",
                    "src"  : "doc://alexa/apl/documents/GridList"
                },
                datasources = datasources2 
              )
            ).response
        )
    
def finish(handler_input):
    return (
        handler_input.response_builder
            .speak("Good bye")
            .set_should_end_session(True)          
            .add_directive( 
              APLRenderDocumentDirective(
                token= "developer-provided-string",
                document = {
                    "type" : "Link",
                    "token" : "my token",
                    "src"  : "doc://alexa/apl/documents/finish"
                }
              )
            ).response
        )
        
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("*****  at handle launch request   *******")
        teams_and_attrs = [["Arsenal", "rgba(255,0,0,1)"], ["Liverpool", "rgba(128,128,0,1)"]]
        #for team in teams_and_attrs:
        #    logger.info(f"Team:{team[0]}, color:{team[1]}, points:{randomize_points(10)}")

        # bucket = "bpltables"
        # logger.info('try to open file ' + bucket + ":" + "line_data")


        # resp = s3.get_object(Bucket=bucket, Key="line_data")
        # body_str = string_data = resp['Body'].read().decode("utf-8")
        # logger.info("converted streaming_body to string")
        # n = body_str.split("\n")
        # lines_in_file = len(n)
        # logger.info(f"there are {len(n)} items in the list")
        # form_data = {}
        # for line in n:
        #     this_line = line.split(',')
        #     form_data[this_line[0]] = this_line[1:]
        # this_team = form_data['chelsea']
        # for points in this_team:
        #     logger.info(f"this weeks points are {points}")


        #logger.info(linedata)
        #logger.info(linedata['visualObjectData'])

        #logger.info(str(get_viewport_profile(handler_input.request_envelope)))
        speech_text = "Welcome to the Alexa APLA demo"

        image_url = "https://duy7y3nglgmh.cloudfront.net/Depositphotos_referee.jpg"
        card = StandardCard(title="Premier League", text="bla", image=Image(small_image_url=image_url, large_image_url=image_url))

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["radioButtonText"] = "Form"
        handler_input.attributes_manager.session_attributes = session_attr
        
        return(handler_input.response_builder.ask("this is the ask").set_card(card).response)






class SimpleTextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SimpleTextIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response"

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text).response
        )






class TextWithEmotionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("TextWithEmotionIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response \
                        <amazon:emotion name=\"excited\" intensity=\"high\"> \
                         with emotion indicators, Liverpool wins the league and so on and so \
                         on emotions take time \
                        </amazon:emotion>"
        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_should_end_session(False).response
        )





class SimpleCardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SimpleCardIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response with a simple card"

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_card(SimpleCard("Hello World", speech_text))
                .set_should_end_session(False).response
        )




class StandardCardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("StandardCardIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "This is a simple spoken response with a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=speech_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .speak(speech_text)
                .set_card(card)
                .set_should_end_session(False).response
        )




class AudioMixIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AudioMixIntent")(handler_input)

    def handle(self, handler_input):
        card_text = "This is a AudioMixed response with a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_card(card)
                .set_should_end_session(False)          
                .add_directive( 
                  RenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_without_data_sources"
                    },
                    datasources = {}              
                  )
                ).response
        )




class AudioMixWithDataSourceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AudioMixWithDataSourceIntent")(handler_input)

    def handle(self, handler_input):
        card_text = "This is a AudioMixed response with data and a standard card"
        image_url = "https://duy7y3nglgmh.cloudfront.net/tackles.png"
        card = StandardCard(title="Premier League", text=card_text, image=Image(small_image_url=image_url, large_image_url=image_url))

        return (
            handler_input.response_builder
                .ask("this is the reprompt")
                .set_card(card)
                .set_should_end_session(False)          
                .add_directive( 
                  RenderDocumentDirective(
                    token= "developer-provided-string",
                    document = {
                        "type" : "Link",
                        "src"  : "doc://alexa/apla/documents/template_with_data_sources"
                    },
                    datasources = {
                        "text": {
                          "speak": "This is the text that will be spoken at the same time the audio \
                          clip plays, it is dynamic and set by the lambda"
                        },
                        "crowd": {
                            "noise": "https://btbscratch.s3.amazonaws.com/FootballCrowdSound.mp3",
                            "start": str(randrange(0, 50*60))
                        }
                    }              
                  )
                ).response
        )




class GridMixIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GridMixIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["radioButtonText"] = "Form"
        handler_input.attributes_manager.session_attributes = session_attr
        this_profile = str(get_viewport_profile(handler_input.request_envelope))
        item_heights = {"ViewportProfile.HUB_LANDSCAPE_SMALL": "75%", "ViewportProfile.HUB_LANDSCAPE_MEDIUM": "65%", "ViewportProfile.HUB_LANDSCAPE_LARGE": "55%"}
        this_height = item_heights.get(this_profile, "")
        
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            datasources2["gridListData"]["listItemHeight"] = this_height
            logger.info(f"** Profile {this_profile} height {this_height}")
            
            return (
                handler_input.response_builder
                    .speak("Welcome to Premier League, press a button or scroll to see more options")
                    .set_should_end_session(False)          
                    .add_directive( 
                      APLRenderDocumentDirective(
                        token= TOKEN,
                        document = {
                            "type" : "Link",
                            "token" : TOKEN,
                            "src"  : "doc://alexa/apl/documents/GridList"
                        },
                        datasources = datasources2 
                      )
                    ).response
                )
        else:
            return (handler_input.response_builder.speak("No screen available, say get table or say a team name").set_should_end_session(False).response)      


class ButtonEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        logger.info("at can handle ButtonEventHandler")
        if is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            user_event = handler_input.request_envelope.request
            return True
        else:
            return False
 
    def handle(self, handler_input):
        SELECTED_COLOR = "white"
        UNSELECTED_COLOR = "grey"
        
        try:
            logger.info("at ButtonEventHandler.handle0 " + str(handler_input.request_envelope.request.arguments[0]))
            logger.info("at ButtonEventHandler.handle1 " + str(handler_input.request_envelope.request.arguments[1]))

        except:
            logger.info("ignore exception")
        first_arg = handler_input.request_envelope.request.arguments[0]

        if first_arg == 'radioButtonText':
            radio_button_id   = handler_input.request_envelope.request.arguments[1]['radioButtonId']
            radio_button_text = handler_input.request_envelope.request.arguments[1]['radioButtonText']
            logger.info(f"about to send an ExecuteCommands based on {handler_input.request_envelope.request.arguments[1]['radioButtonId']}")
            buttons = ["Form","Results","Fixtures"]
            texts   = ["ShowTeamForm","ShowTeamResults","ShowTeamFixtures"]
            button_commands = []
            
            # for each button turn it on/off based on what was picked
            for button, button_text in zip(buttons,texts):  
                value = SELECTED_COLOR if handler_input.request_envelope.request.arguments[1]['radioButtonId'] == button else UNSELECTED_COLOR
                set_value_command = SetValueCommand(component_id=button,object_property="radioButtonColor",value=value)
                button_commands.append(set_value_command)
                
                logger.info(f"setting {button_text} to {value}")
                set_value_command = SetValueCommand(component_id=button_text,object_property="color",value=value)
                button_commands.append(set_value_command)

                value = True if handler_input.request_envelope.request.arguments[1]['radioButtonId'] == button else False
                if value == True:
                    # remember what button was selected for the next event
                    session_attr = handler_input.attributes_manager.session_attributes
                    session_attr["radioButtonText"] = handler_input.request_envelope.request.arguments[1]['radioButtonId']
                    handler_input.attributes_manager.session_attributes = session_attr

                set_value_command = SetValueCommand(component_id=button,object_property="checked",value=value)
                button_commands.append(set_value_command)
            return (handler_input.response_builder.speak(f"Ok, we'll show you team {radio_button_id}").add_directive(ExecuteCommandsDirective(token=TOKEN,commands=button_commands)).response)
            

        if first_arg == "goBack":
            return(go_home(handler_input))
            
        if first_arg == "teams":
            this_profile = str(get_viewport_profile(handler_input.request_envelope))
            item_heights = {"ViewportProfile.HUB_LANDSCAPE_SMALL": "75%", "ViewportProfile.HUB_LANDSCAPE_MEDIUM": "65%", "ViewportProfile.HUB_LANDSCAPE_LARGE": "55%"}
            this_height = item_heights.get(this_profile, "")
            teamsdatasource["gridListData"]["listItemHeight"] = this_height
            return (
                handler_input.response_builder
                    .speak("Here is the page of just teams")
                    .set_should_end_session(False)          
                    .add_directive( 
                      APLRenderDocumentDirective(
                        token= TOKEN,
                        document = {
                            "type" : "Link",
                            "token" : TOKEN,
                            "src"  : "doc://alexa/apl/documents/RadioButtons"
                        },
                        datasources = teamsdatasource 
                      )
                    ).response
                )
            
        session_attr = handler_input.attributes_manager.session_attributes

        # if we get here it was an actual button press so we should say something
        return say_stats(handler_input,test_speach_data.get(first_arg, first_arg + ", " + session_attr.get("radioButtonText", "")))

class AddTeamIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AddTeamIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Add handler")
        return(add_or_delete_team(handler_input, "add"))

class RemoveTeamIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RemoveTeamIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Remove handler")
        return(add_or_delete_team(handler_input, "remove"))


'''
The voice model has one slot but that slot is marked as can accept multiple values.
So, the slot value might be in one part of the handler_input or a different part
'''
def add_or_delete_team(handler_input, mode):
    slot = get_slot(handler_input, "plteam")
    if slot.resolutions is not None:    # there is only one slot value
        dict = slot.resolutions.to_dict()
        logger.info("Team name is: " + dict['resolutions_per_authority'][0]["values"][0]["value"]["name"])
        team = dict['resolutions_per_authority'][0]["values"][0]["value"]["name"]
        session_attr = handler_input.attributes_manager.session_attributes
        if mode == "add":
            session_attr[team] = True
            logger.info(f"added team {team} to the session")
        else:
            session_attr.pop(team, "not found ")
            logger.info(f"removed team {team} to the session")
        handler_input.attributes_manager.session_attributes = session_attr
        return(load_and_output_graph(handler_input, linedata))

    else:  # there are multiple slot values
        session_attr = handler_input.attributes_manager.session_attributes
        for value in slot.slot_value.values:
            logger.info("Team Name: " + str(value.resolutions.resolutions_per_authority[0].values[0].value.name))
            team = str(value.resolutions.resolutions_per_authority[0].values[0].value.name)
            if mode == "add":
                session_attr[team] = True
                logger.info(f"added team {team} to the session")
            else:
                session_attr.pop(team, "not found 2")
                logger.info(f"removed team {team} to the session")
        handler_input.attributes_manager.session_attributes = session_attr
        return(load_and_output_graph(handler_input, linedata))


class LineChartIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LineChartIntent")(handler_input)

    def handle(self, handler_input):
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            return(load_and_output_graph(handler_input, linedata))
        else:
            return (handler_input.response_builder.speak("No screen available, say get table or say a team name").set_should_end_session(False).response)      

class LineChartWithTeamIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LineChartWithTeamsIntent")(handler_input)

    def handle(self, handler_input):
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            add_or_delete_team(handler_input, "add")
            return(load_and_output_graph(handler_input, linedata))
        else:
            return (handler_input.response_builder.speak("No screen available, say get table or say a team name").set_should_end_session(False).response)      


''' zero points for a loss, 1 point for a draw and 3 points for a win '''
def randomize_points(num_points):
    points = [0]
    possible_points = [0,1,3]
    for x in range(1,num_points):
        points.append( points[x-1] + possible_points[randrange(3) ])
    return(points)
    
def get_team_points_and_color():
    resp = s3.get_object(Bucket=bucket, Key="line_data")
    body_str = string_data = resp['Body'].read().decode("utf-8")
    logger.info("converted streaming_body to string")
    n = body_str.split("\n")
    n.pop()
    lines_in_file = len(n)
    logger.info(f"there are {len(n)} items in the list")
    form_data = {}
    for line in n:
        this_line = line.split(',')
        form_data[this_line[0]] = this_line[1:]
    return form_data
    #this_team = form_data['chelsea']
    #for points in this_team:
    #    logger.info(f"this weeks points are {points}")

def random_color():
    #"rgba(239,1,7,1)"
    return f"rgba({randrange(255)},{randrange(255)},{randrange(255)},1)"
    
'''
This routine would hold the business logic to provide the actual data for the graph
'''
def load_and_output_graph(handler_input, linedata):
    NUM_POINTS = 20
    MAX_POINTS = 40
    create_ticks(NUM_POINTS, linedata)
    create_verticle_ticks(4, linedata)
    session_attr = handler_input.attributes_manager.session_attributes
    linedata['visualObjectData']['lineChartData']['paths'] = []
    form_data = get_team_points_and_color()
    
    # teams_and_attrs = [["Arsenal",           "rgba(239,1,7,1)"], 
    #                   ["Liverpool",         "rgba(208,0,39,1)"],
    #                   ["Leicester City",    "rgba(253,190,17,1)"],
    #                   ["Chelsea",           "rgba(3,70,148,1)"],
    #                   ["Manchester City",   "rgba(108,173,223,1)"],
    #                   ["Manchester United", "rgba(255,229,0,1)"],
    #                   ["Brentford",         "rgba(128,255,255,1)"],
    #                   ["Everton",           "rgba(39,68,136,1)"],
    #                   ]
    logger.info("about to search for active teams in " + str(form_data))
    for team, points in form_data.items():
    #for team in form_data:
        logger.info(f"Team:{team}, points:{points}")
        name = session_attr.get(team, None)
        if name is not None:
            logger.info(f"Team {team} is active, get its points and graph it")
            this_team = form_data.get(team, "not found")
            logger.info("this team:" + str(this_team))
            logger.info("team " + str(team) + " " + str(points))
            logger.info("formdata " + str(form_data))
            load_points(linedata,  points,                               team,   random_color(), MAX_POINTS)
            #load_points(linedata, randomize_points(min(38,NUM_POINTS)), team[0], team[1],              MAX_POINTS)
            
    say = "Say add or remove"    
    return (
        handler_input.response_builder
            .speak(say)
            .set_should_end_session(False)          
            .add_directive( 
              APLRenderDocumentDirective(
                token= TOKEN,
                document = {
                    "type" : "Link",
                    "token" : TOKEN,
                    "src"  : "doc://alexa/apl/documents/LineChart"
                },
                datasources = linedata 
              )
            ).response
        )
    
    
''' verticle range is 1 to 0 with 0 at the top, so divide that by max_points to get verticle per point, then 1 - that value'''
def load_points(linedata, team_points, team_name, color, max_points):
    y_per_point = 1.0 / max_points
    X_POS = 2.0 / len(team_points)
    logger.info("in load_points, team_points is: " + str(team_points))
    points = []
    for index in range(len(team_points)):
        logger.info(f"at {index}: {team_points[index]}")
        points.append({'x': X_POS * index, 'y': 1.0 - (int(team_points[index]) * y_per_point)}) 
    
    logger.info(f"points {points}")
    team_path = {"label": team_name, "points": points, "pathColor": color}
    linedata['visualObjectData']['lineChartData']['paths'].append(team_path)    

    
def create_ticks(num_ticks, linedata):
    logger.info("creating ticks by two")
    TICK_SPACE = 1 / num_ticks
    ticks = []
    for index in range(0,num_ticks,2):
        comp_inner = {"type" : "Text", "textValue" : str(index), "width": TICK_WIDTH}
        comp = {"component": comp_inner, "space": TICK_SPACE * index}
        ticks.append(comp)
    linedata['visualObjectData']['lineChartData']['primaryTickList']['ticks'] = ticks    


def create_verticle_ticks(num_ticks, linedata):
    logger.info(linedata)
    ticks = []
    for index in range(num_ticks):
        comp_inner = {"type" : "Text", "textValue" : str(index*10), "width": TICK_WIDTH}
        comp = {"component": comp_inner, "space": index*0.25}
        ticks.append(comp)
    linedata['visualObjectData']['lineChartData']['defaultValueTickList']['ticks'] = ticks    


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speech_text = "Goodbye!"

        # handler_input.response_builder.speak(speech_text).set_card(
        #     SimpleCard("Hello World", speech_text))
        # return handler_input.response_builder.response
        return(finish(handler_input))


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("can_handle fallback")
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("handle fallback")
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #return handler_input.response_builder.response
        return(finish(handler_input))


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Alexa Request was: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Alexa Response: {}".format(response))

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SimpleTextIntentHandler())
sb.add_request_handler(TextWithEmotionIntentHandler())
sb.add_request_handler(SimpleCardIntentHandler())
sb.add_request_handler(StandardCardIntentHandler())
sb.add_request_handler(AudioMixIntentHandler())
sb.add_request_handler(GridMixIntentHandler())
sb.add_request_handler(ButtonEventHandler())
sb.add_request_handler(AudioMixWithDataSourceIntentHandler())
sb.add_request_handler(LineChartIntentHandler())
sb.add_request_handler(LineChartWithTeamIntentHandler())
sb.add_request_handler(AddTeamIntentHandler())
sb.add_request_handler(RemoveTeamIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
#sb.add_global_request_interceptor(RequestLogger())
#sb.add_global_response_interceptor(ResponseLogger())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
