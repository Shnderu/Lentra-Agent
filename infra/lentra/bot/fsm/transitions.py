from lentra.bot.fsm.states import *


ALLOWED_TRANSITIONS = {

    IDLE: {
        SEARCHING
    },

    SEARCHING: {
        LIST
    },

    LIST: {
        DETAIL,
        FILTERS,
        FAVORITES,
        PROFILE
    },

    DETAIL: {
        LIST,
        FAVORITES
    },

    FILTERS: {
        LIST
    },

    FAVORITES: {
        DETAIL,
        LIST
    },

    PROFILE: {
        LIST
    }
}
