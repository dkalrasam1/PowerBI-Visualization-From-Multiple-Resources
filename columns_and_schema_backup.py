

schema = {}

conversion_conv = [
    "quality_issues"
]


account_overview_schema = [
    {

        "name": "average_call_duration",
        "type": "INTEGER"

    },
    {

        "name": "average_callback_wait_time",
        "type": "INTEGER"

    },
    {
        "name": "average_hold_time",
        "type": "INTEGER"
    },
    {

        "name": "average_queue_wait_time",
        "type": "INTEGER"

    },
    {
        "name": "average_time_to_answer",
        "type": "INTEGER"
    },
    {

        "name": "average_wrap_up_time",
        "type": "INTEGER"

    },
    {
        "name": "max_calls_waiting",
        "type": "INTEGER"
    },
    {
        "name": "max_queue_wait_time",
        "type": "INTEGER"
    },
    {
        "name": "total_call_duration",
        "type": "INTEGER"

    },
    {
        "name": "total_callback_calls",
        "type": "INTEGER"
    },
    {
        "name": "total_calls",
        "type": "INTEGER"
    },
    {
        "name": "total_calls_abandoned_in_queue",
        "type": "INTEGER"
    },
    {
        "name": "total_calls_outside_business_hours",
        "type": "INTEGER"
    },
    {
        "name": "total_calls_with_exceeded_queue_wait_time",
        "type": "INTEGER"
    },
    {
        "name": "total_calls_with_requested_voicemail",
        "type": "INTEGER"
    },
    {
        "name": "total_embeddable_callback_calls",
        "type": "INTEGER"
    },
    {
        "name": "total_hold_time",
        "type": "INTEGER"
    },
    {
        "name": "total_inbound_calls",
        "type": "INTEGER"
    },
    {
        "name": "total_outbound_calls",
        "type": "INTEGER"
    },
    {
        "name": "total_textback_requests",
        "type": "INTEGER"
    },
    {
        "name": "total_voicemails",
        "type": "INTEGER"
    },
    {
        "name": "total_wrap_up_time",
        "type": "INTEGER"
    },
    {
        "name": "date",
        "type": "DATE"
    }

]


incremental_call = [
    {
        "name": "id",
        "type": "INTEGER"

    },
    {
        "name": "created_at",
        "type": "TIMESTAMP"
    },
    {
        "name": "updated_at",
        "type": "TIMESTAMP"
    },
    {
        "name": "agent_id",
        "type": "INTEGER"
    },
    {
        "name": "call_charge",
        "type": "FLOAT"
    },
    {
        "name": "consultation_time",
        "type": "INTEGER"
    },
    {
        "name": "completion_status",
        "type": "STRING"
    },
    {
        "name": "customer_id",
        "type": "INTEGER"
    },
    {
        "name": "customer_requested_voicemail",
        "type": "BOOLEAN"
    },
    {
        "name": "direction",
        "type": "STRING"
    },
    {
        "name": "duration",
        "type": "INTEGER"
    },
    {
        "name": "exceeded_queue_wait_time",
        "type": "BOOLEAN"
    },
    {
        "name": "hold_time",
        "type": "INTEGER"
    },
    {
        "name": "minutes_billed",
        "type": "INTEGER"
    },
    {
        "name": "outside_business_hours",
        "type": "BOOLEAN"
    },
    {
        "name": "phone_number_id",
        "type": "INTEGER"
    },
    {
        "name": "phone_number",
        "type": "INTEGER"
    },
    {
        "name": "ticket_id",
        "type": "INTEGER"
    },
    {
        "name": "time_to_answer",
        "type": "INTEGER"
    },
    {
        "name": "voicemail",
        "type": "BOOLEAN"
    },
    {
        "name": "wait_time",
        "type": "INTEGER"
    },
    {
        "name": "wrap_up_time",
        "type": "INTEGER"
    },
    {
        "name": "ivr_time_spent",
        "type": "INTEGER"
    },
    {
        "name": "ivr_hops",
        "type": "INTEGER"
    },
    {
        "name": "ivr_destination_group_name",
        "type": "STRING"
    },
    {
        "name": "talk_time",
        "type": "INTEGER"
    },
    {
        "name": "ivr_routed_to",
        "type": "INTEGER"
    },
    {
        "name": "callback",
        "type": "BOOLEAN"
    },
    {
        "name": "callback_source",
        "type": "STRING"
    },
    {
        "name": "default_group",
        "type": "BOOLEAN"
    },
    {
        "name": "ivr_action",
        "type": "STRING"
    },
    {
        "name": "overflowed",
        "type": "BOOLEAN"
    },
    {
        "name": "overflowed_to",
        "type": "STRING"
    },
    {
        "name": "recording_control_interactions",
        "type": "INTEGER"
    },
    {
        "name": "recording_time",
        "type": "INTEGER"
    },
    {
        "name": "not_recording_time",
        "type": "INTEGER"
    },
    {
        "name": "call_recording_consent",
        "type": "STRING"
    },
    {
        "name": "call_recording_consent_action",
        "type": "STRING"
    },
    {
        "name": "call_recording_consent_keypress",
        "type": "STRING"
    },
    {
        "name": "call_group_id",
        "type": "INTEGER"
    },
    {
        "name": "call_channel",
        "type": "STRING"
    },
    {
        "name": "quality_issues",
        "type": "STRING",
        "mode":"REPEATED"
    }

]

file_upload = [

    {
        "name": "table_name",
        "type": "STRING"
    },
    {
        "name": "date",
        "type": "DATE"
    }
]


agents_activity_schema = [
    {
        "name": "name",
        "type": "STRING"
    },
    {
        "name": "agent_id",
        "type": "INTEGER"
    },
    {
        "name": "via",
        "type": "STRING"

    },
    {
        "name": "avatar_url",
        "type": "STRING"
    },
    {
        "name": "forwarding_number",
        "type": "INTEGER"
    },
    {
        "name": "average_talk_time",
        "type": "INTEGER"
    },
    {
        "name": "calls_accepted",
        "type": "INTEGER"
    },
    {
        "name": "calls_denied",
        "type": "INTEGER"
    },
    {
        "name": "calls_missed",
        "type": "INTEGER"
    },
    {
        "name": "online_time",
        "type": "INTEGER"
    },
    {
        "name": "available_time",
        "type": "INTEGER"
    },
    {
        'name': "total_call_duration",
        "type": "INTEGER"
    },
    {
        "name": "total_talk_time",
        "type": "INTEGER"
    },
    {
        "name": "total_wrap_up_time",
        "type": "INTEGER"
    },
    {
        "name": "away_time",
        "type": "INTEGER"
    },
    {
        "name": "call_status",
        "type": "STRING"
    },
    {
        "name": "agent_state",
        "type": "STRING"
    },
    {
        "name": "transfers_only_time",
        "type": "INTEGER"
    },
    {
        "name": "average_wrap_up_time",
        "type": "INTEGER"
    },
    {
        "name": "accepted_transfers",
        "type": "INTEGER"
    },
    {
        "name": "started_transfers",
        "type": "INTEGER"
    },
    {
        "name": "calls_put_on_hold",
        "type": "INTEGER"
    },
    {
        "name": "average_hold_time",
        "type": "INTEGER"
    },
    {
        "name": "total_hold_time",
        "type": "INTEGER"
    },
    {
        "name": "started_third_party_conferences",
        "type": "INTEGER"
    },
    {
        "name": "accepted_third_party_conferences",
        "type": "INTEGER"
    },
    {
        "name":"uploaded_on",
        "type":"DATE"
    }

]

menus_schema = [

    {
        "name":"id",
        "type":"STRING"
    },
    {
        "name":"name",
        "type":"STRING"
    },
    {
        "name":"default",
        "type":"BOOLEAN"
    },
    {
        "name":"greeting_id",
        "type":"INTEGER"
    },
    {
        "name":"routes",
        "type":"records"
    }


]




schema["account_overview"] = account_overview_schema
schema["incremental_calls"] = incremental_call
schema["agents_activity"] = agents_activity_schema








