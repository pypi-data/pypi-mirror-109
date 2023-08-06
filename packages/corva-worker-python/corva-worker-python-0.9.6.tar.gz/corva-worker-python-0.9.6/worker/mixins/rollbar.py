import os
import sys


class RollbarMixin(object):
    def __init__(self, *args, **kwargs):
        self.rollbar = kwargs.pop('rollbar', None)
        super().__init__(*args, **kwargs)

    def is_rollbar(self) -> bool:
        """
        To check if rollbar is available or not
        :return: if rollbar is available
        """
        return self.rollbar and self.rollbar.SETTINGS.get('enabled')

    def track_message(self, message: str, level: str):
        """
        To send a message to rollbar
        :param message:
        :param level: any of the following levels:
        ['critical', 'error', 'warning', 'info', 'debug', 'ignored']
        :return:
        """
        # Levels:
        if not self.is_rollbar():
            print(f"{level} - {message}")
            return

        level = level.lower()

        self.rollbar.report_message(message, level)

    def track_error(self, message: str = None):
        if not self.is_rollbar():
            raise

        self.rollbar.report_exc_info(extra_data=message, level='error')


def payload_handler(payload: dict, **kw) -> dict:  # kw is currently unused
    """
    This is a rollbar payload handler which will be called on every payload being sent to rollbar
    This handler has to be added to rollbar instance after init
    The aim is to smartly trim the payload being sent to rollbar
    Use like -> rollbar.events.add_payload_handler(payload_handler)
    To pause trimming set REDUCED_ROLLBAR_PAYLOAD to False or false in env variables

    :param payload: Payload automatically captured based on exc, args and locals
    :param kw:
    :return: Trimmed payload
    """
    reduced_rollbar_payload_flag = os.getenv("REDUCED_ROLLBAR_PAYLOAD", "true").lower()

    # If REDUCED_ROLLBAR_PAYLOAD is set to False or false in env variables, trimming will be paused
    if reduced_rollbar_payload_flag == "false":
        return payload

    try:
        payload_frames = payload["data"]["body"]["trace"].pop("frames", [])
    except KeyError:
        return payload

    def should_trim_dictionary(di: dict) -> bool:
        """
        This function returns True if dict is larger than 50kb and has key "data"
        """
        return isinstance(di, dict) and sys.getsizeof(di) / 1024 > 50 and "data" in di.keys()

    removed_payload_message = "removed due to large payload"

    # All the locals are nested inside frames.
    # Smartly payload reduce size
    for frame in payload_frames:
        local_vars = frame.get("locals", {})
        for key, value in local_vars.items():
            # If len of list is greater than 20, retain the first and last element
            # TODO: Use walrus operator for list_length once all apps move to python 3.8+
            if isinstance(value, list) and len(value) > 20:
                local_vars[key] = value[::len(value) - 1]
                local_vars[key].insert(1, removed_payload_message)

                # If any element of the list greater than 50 kb, drop the data component
                for each in value:
                    if should_trim_dictionary(each):
                        each["data"] = removed_payload_message

            # If in memory size of dict is greater than 50kb, drop the data component
            elif should_trim_dictionary(value):
                value["data"] = removed_payload_message

    payload["data"]["body"]["trace"]["frames"] = payload_frames
    return payload
