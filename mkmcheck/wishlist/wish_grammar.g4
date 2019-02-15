
grammar wish_grammar;




start : wish EOF;

wish :
    cardboard_wishes #WishNoMeta
    | meta cardboard_wishes #WishWithMeta
;

meta :
    '(' inclution_strategy ')'
;

inclution_strategy:
    EXCLUDE_PARTIALLY_FULFILLED #ExcludePartiallyFulfilled
    | INCLUDE_PARTIALLY_FULFILLED #IncludePartiallyFulfilled
;

cardboard_wishes :
    cardboard_wish #CardboardWishBase
    | cardboard_wish ';' cardboard_wishes #CardboardWishChain
;


cardboard_wish :
    required_cardboard #RequiredCardboardNoAmount
    | INTEGER '#' required_cardboard #RequiredCardboardWithAmount
;

required_cardboard:
    VALUE #RequiredCardboardNoRequirements
    | VALUE '(' requirements ')' #RequiredCardboardWithRequirements
;

requirements :
    requirement #RequirementBase
    | requirements ';' requirement #RequirementChain
;

requirement :
    FROM_EXPANSIONS REQUIREMENT_VALUE_SEPERATOR expansions #FromExpansions
    | IS_BORDER REQUIREMENT_VALUE_SEPERATOR border #IsBorder
    | IS_MINIMUM_CONDITION REQUIREMENT_VALUE_SEPERATOR condition #IsMinimumCondition
    | IS_LANGUAGE REQUIREMENT_VALUE_SEPERATOR language #IsLanguage
    | IS_FOIL REQUIREMENT_VALUE_SEPERATOR boolean #IsFoil
    | IS_ALTERED REQUIREMENT_VALUE_SEPERATOR boolean #IsAltered
    | IS_SIGNED REQUIREMENT_VALUE_SEPERATOR boolean #IsSigned

    | ANY_LANGUAGE #AnyLanguage
    | CAN_BE_FOIL #CanBeFoil
    | CAN_BE_ALTERED #CanBeAltered
    | CAN_BE_SIGNED #CanBeSigned
;

expansions :
    EXPANSION_CODE_VALUE #Expansion
    | expansions ',' EXPANSION_CODE_VALUE #ExpansionChain
;

boolean :
    TRUE #BooleanTrue
    | FALSE #BooleanFalse
;

border :
    WHITE_BORDER #WhiteBorder
    | BLACK_BORDER #BlackBorder
    | SILVER_BORDER #SilverBorder
    | GOLD_BORDER #GoldBorder
;

condition :
    MINT #Mint
    | NEAR_MINT #NearMint
    | EXCELLENT #Excellent
    | GOOD #Good
    | LIGHT_PLAYED #LightPlayed
    | PLAYED # Played
    | POOR #Poor
;

language :
    ENGLISH #English
    | FRENCH #French
    | GERMAN #German
    | SPANISH #Spanish
    | ITALIAN #Italian
    | SIMPLIFIED_CHINESE #SimplifiedChinese
    | JAPANESE #Japanese
    | PORTUGUESE #Portuguese
    | RUSSIAN #Japanese
    | KOREAN #Korean
    | TRADITIONAL_CHINESE #TraditionalChinese
;

INTEGER : [0-9]+;

EXPANSION_CODE_VALUE : [A-Z0-9_]+;

TRUE : 'true';
FALSE : 'false';

WHITE_BORDER : 'white';
BLACK_BORDER : 'black';
SILVER_BORDER : 'silver';
GOLD_BORDER : 'gold';

MINT : 'mint';
NEAR_MINT : 'near_mint';
EXCELLENT : 'excellent';
GOOD : 'good';
LIGHT_PLAYED : 'light_played';
PLAYED : 'played';
POOR : 'poor';

ENGLISH : 'english';
FRENCH : 'french';
GERMAN : 'german';
SPANISH : 'spanish';
ITALIAN : 'italian';
SIMPLIFIED_CHINESE : 'simplified_chinese';
JAPANESE : 'japanese';
PORTUGUESE : 'portguese';
RUSSIAN : 'russian';
KOREAN : 'korean';
TRADITIONAL_CHINESE : 'traditional_chinese';

EXCLUDE_PARTIALLY_FULFILLED : 'exclude_partially_fulfilled';
INCLUDE_PARTIALLY_FULFILLED : 'include_partially_fulfilled';

REQUIREMENT_VALUE_SEPERATOR : '|';

FROM_EXPANSIONS : 'from_expansions';
IS_BORDER : 'is_border';
IS_MINIMUM_CONDITION : 'is_minimum_condition';
IS_LANGUAGE : 'is_language';
IS_FOIL : 'is_foil';
IS_ALTERED : 'is_altered';
IS_SIGNED : 'is_signed';

ANY_LANGUAGE : 'any_language';
CAN_BE_FOIL : 'can_be_foil';
CAN_BE_ALTERED : 'can_be_altered';
CAN_BE_SIGNED : 'can_be_signed';

VALUE : [a-zA-Z0-9':/!âáéàíúöû,_-][a-zA-Z0-9':/!âáéàíúöû,_ -]*[a-zA-Z0-9':/!âáéàíúöû,_-];

WHITESPACE : [ \n\t\r] -> skip;