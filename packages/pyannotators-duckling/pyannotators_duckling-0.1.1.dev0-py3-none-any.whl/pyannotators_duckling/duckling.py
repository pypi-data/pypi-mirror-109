from typing import Type, List, cast

import pendulum
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation
from duckling import (load_time_zones, parse_ref_time,
                      parse_lang, default_locale_lang, parse_locale,
                      parse_dimensions, parse, Context)


class DucklingParameters(AnnotatorParameters):
    time_zone: str = Field("Europe/Paris",
                           description="Reference time zone to normalize date/time, must be a valid linux file in /usr/share/zoneinfo")
    lang: str = Field("fr", description="Reference language")
    locale: str = Field("fr_FR", description="Reference locale")
    dimensions = Field(
        "amount-of-money,credit-card-number,distance,duration,email,phone-number,quantity,temperature,time,time-grain,url,volume",
        description="""Comma-separated list of [Duckling](https://github.com/facebook/duckling) dimensions to consider, to be chosen among:<br/>
        <li>amount-of-money: Measures an amount of money such as *$20*, *30 euros*.
        <li>credit-card-number: Captures a credit card number.
        <li>distance: Captures a distance in miles or kilometers such as *5km*, *5 miles* and *12m*.
        <li>duration: Captures a duration such as *30min*, *2 hours* or *15sec* and normalizes the value in seconds.
        <li>email: Captures an email but do not try to check the validity of the email. For example, *support@kairntech.com*.
        <li>number: Extrapolates a number from free text, such as *six*,*twelve*, *16*, *1.10* and *23K*.
        <li>ordinal: Captures the measure of an ordinal number, such as *first*, *second*, *third*... or *1st*, *2nd*, ..., *7th*, etc.
        <li>phone-number: Captures phone numbers, but does not try to check the validity of the number.
        <li>quantity: Captures the quantity of something; such as ingredients in recipes, or quantities of food for health tracking apps. Returns a numerical value, a unit, and a product (each field is optional).
        <li>temperature: Captures the temperature in units of celsius or fahrenheit degrees.
        <li>time: Captures and resolves date and time, like *tomorrow at 6pm*.
        <li>url: Captures an URL, but does not try to check the validity of the URL.
        <li>volume: Captures measures of volume like *250 ml*, *3 gal*.
        """)


class DucklingAnnotator(AnnotatorBase):
    """[Duckling](https://github.com/facebook/duckling) annotator.
    """
    time_zones = load_time_zones("/usr/share/zoneinfo")

    def annotate(self, documents: List[Document], parameters: AnnotatorParameters) \
            -> List[Document]:
        params: DucklingParameters = \
            cast(DucklingParameters, parameters)
        # Load reference time for time parsing
        time_zones = load_time_zones("/usr/share/zoneinfo")
        bog_now = pendulum.now(params.time_zone).replace(microsecond=0)
        ref_time = parse_ref_time(
            time_zones, params.time_zone, bog_now.int_timestamp)

        # Load language/locale information
        lang = parse_lang(params.lang)
        default_locale = default_locale_lang(lang)
        locale = parse_locale(params.locale, default_locale)

        # Create parsing context with time and language information
        context = Context(ref_time, locale)

        # Define dimensions to look-up for
        valid_dimensions = [d.strip() for d in params.dimensions.split(",")]

        # Parse dimensions to use
        output_dims = parse_dimensions(valid_dimensions)

        for document in documents:
            document.annotations = []
            if not document.sentences:
                document.sentences = [Span(start=0, end=len(document.text))]
            for sent in document.sentences:
                # Parse a phrase
                dims = parse(document.text[sent.start:sent.end], context, output_dims, False)
                for dim in dims:
                    document.annotations.append(Annotation(start=sent.start + dim['start'], end=sent.start + dim['end'],
                                                           labelName=dim['dim'].replace('-', '_'), label=dim['dim'],
                                                           text=dim['body'],
                                                           properties=dim['value']))
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DucklingParameters
