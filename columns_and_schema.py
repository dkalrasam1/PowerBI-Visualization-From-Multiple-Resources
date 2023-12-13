from google.cloud.bigquery import SchemaField
import os

#os.chdir("/home/dashboards/cron_scripts")
os.chdir("/var/www/html/zugo_bikes")

schema = {}

agents_activity = [
    SchemaField('name', 'STRING'), SchemaField('agent_id', 'INTEGER'),
    SchemaField('via', 'STRING'), SchemaField(
        'avatar_url', 'STRING'),
    SchemaField('forwarding_number', 'INTEGER'), SchemaField(
        'average_talk_time', 'INTEGER'),
    SchemaField('calls_accepted', 'INTEGER'), SchemaField(
        'calls_denied', 'INTEGER'),
    SchemaField('calls_missed', 'INTEGER'), SchemaField(
        'online_time', 'INTEGER'),
    SchemaField('available_time', 'INTEGER'), SchemaField(
        'total_call_duration', 'INTEGER'),
    SchemaField('total_talk_time', 'INTEGER'), SchemaField(
        'total_wrap_up_time', 'INTEGER'), SchemaField('away_time', 'INTEGER'),
    SchemaField('call_status', 'STRING'), SchemaField('agent_state', 'STRING'),
    SchemaField('transfers_only_time', 'INTEGER'),
    SchemaField('average_wrap_up_time', 'INTEGER'),
    SchemaField('accepted_transfers', 'INTEGER'), SchemaField(
        'started_transfers', 'INTEGER'),
    SchemaField('calls_put_on_hold', 'INTEGER'),
    SchemaField('average_hold_time', 'INTEGER'),
    SchemaField('total_hold_time', 'INTEGER'),
    SchemaField('started_third_party_conferences', 'INTEGER'),
    SchemaField('accepted_third_party_conferences', 'INTEGER')
]

incremental_calls = [SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('created_at', 'TIMESTAMP', 'NULLABLE'), SchemaField('updated_at', 'TIMESTAMP', 'NULLABLE'), SchemaField('agent_id', 'INTEGER', 'NULLABLE'), SchemaField('call_charge', 'FLOAT', 'NULLABLE'), SchemaField('consultation_time', 'INTEGER', 'NULLABLE'), SchemaField('completion_status', 'STRING', 'NULLABLE'), SchemaField('customer_id', 'INTEGER', 'NULLABLE'), SchemaField('customer_requested_voicemail', 'BOOLEAN', 'NULLABLE'), SchemaField('direction', 'STRING', 'NULLABLE'), SchemaField('duration', 'INTEGER', 'NULLABLE'), SchemaField('exceeded_queue_wait_time', 'BOOLEAN', 'NULLABLE'), SchemaField('hold_time', 'INTEGER', 'NULLABLE'), SchemaField('minutes_billed', 'INTEGER', 'NULLABLE'), SchemaField('outside_business_hours', 'BOOLEAN', 'NULLABLE'), SchemaField('phone_number_id', 'INTEGER', 'NULLABLE'), SchemaField('phone_number', 'INTEGER', 'NULLABLE'), SchemaField('ticket_id', 'INTEGER', 'NULLABLE'), SchemaField('time_to_answer', 'INTEGER', 'NULLABLE'), SchemaField('voicemail', 'BOOLEAN', 'NULLABLE'), SchemaField('wait_time', 'INTEGER', 'NULLABLE'), SchemaField(
    'wrap_up_time', 'INTEGER', 'NULLABLE'), SchemaField('ivr_time_spent', 'INTEGER', 'NULLABLE'), SchemaField('ivr_hops', 'INTEGER', 'NULLABLE'), SchemaField('ivr_destination_group_name', 'STRING', 'NULLABLE'), SchemaField('talk_time', 'INTEGER', 'NULLABLE'), SchemaField('ivr_routed_to', 'INTEGER', 'NULLABLE'), SchemaField('callback', 'BOOLEAN', 'NULLABLE'), SchemaField('callback_source', 'STRING', 'NULLABLE'), SchemaField('default_group', 'BOOLEAN', 'NULLABLE'), SchemaField('ivr_action', 'STRING', 'NULLABLE'), SchemaField('overflowed', 'BOOLEAN', 'NULLABLE'), SchemaField('overflowed_to', 'STRING', 'NULLABLE'), SchemaField('recording_control_interactions', 'INTEGER', 'NULLABLE'), SchemaField('recording_time', 'INTEGER', 'NULLABLE'), SchemaField('not_recording_time', 'INTEGER', 'NULLABLE'), SchemaField('call_recording_consent', 'STRING', 'NULLABLE'), SchemaField('call_recording_consent_action', 'STRING', 'NULLABLE'), SchemaField('call_recording_consent_keypress', 'STRING', 'NULLABLE'), SchemaField('call_group_id', 'INTEGER', 'NULLABLE'), SchemaField('call_channel', 'STRING', 'NULLABLE'),
    SchemaField('quality_issues', 'STRING', 'REPEATED')]

menu_routes = [SchemaField('options', 'RECORD', 'NULLABLE', (SchemaField('group_ids', 'INTEGER', 'REPEATED'),)), SchemaField('overflow_options', 'STRING', 'REPEATED'), SchemaField('greeting', 'STRING', 'NULLABLE'), SchemaField(
    'option_text', 'STRING', 'NULLABLE'), SchemaField('action', 'STRING', 'NULLABLE'), SchemaField('keypress', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE')]

menus = [SchemaField('default', 'BOOLEAN', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('routes', 'RECORD', 'REPEATED', (SchemaField('options', 'RECORD', 'NULLABLE', (SchemaField('group_ids', 'INTEGER', 'REPEATED'),)), SchemaField('overflow_options', 'STRING', 'REPEATED'), SchemaField(
    'greeting', 'STRING', 'NULLABLE'), SchemaField('option_text', 'STRING', 'NULLABLE'), SchemaField('action', 'STRING', 'NULLABLE'), SchemaField('keypress', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'))), SchemaField('greeting_id', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE')]

voice_ivr = [SchemaField('phone_number_names', 'STRING', 'REPEATED'), SchemaField('phone_number_ids', 'INTEGER', 'REPEATED'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('menus', 'RECORD', 'REPEATED', (SchemaField('default', 'BOOLEAN', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('routes', 'RECORD', 'REPEATED', (SchemaField('options', 'RECORD', 'NULLABLE', (SchemaField('group_ids', 'INTEGER', 'REPEATED'),)), SchemaField(
    'overflow_options', 'STRING', 'REPEATED'), SchemaField('greeting', 'STRING', 'NULLABLE'), SchemaField('option_text', 'STRING', 'NULLABLE'), SchemaField('action', 'STRING', 'NULLABLE'), SchemaField('keypress', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'))), SchemaField('greeting_id', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'))), SchemaField('id', 'INTEGER', 'NULLABLE')]


shopify_orders = [SchemaField('shipping_address_province', 'STRING', 'NULLABLE'), SchemaField('shipping_address_country', 'STRING', 'NULLABLE'), SchemaField('shipping_address_zip', 'STRING', 'NULLABLE'), SchemaField('shipping_address_city', 'STRING', 'NULLABLE'),
 SchemaField('total_shipping_price_set_shop_money_amount', 'FLOAT', 'NULLABLE'), SchemaField('tags', 'STRING', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('source_name', 'STRING', 'NULLABLE'), SchemaField('updated_at', 'TIMESTAMP', 'NULLABLE'), SchemaField('fulfillment_status', 'STRING', 'NULLABLE'), SchemaField('financial_status', 'STRING', 'NULLABLE'), SchemaField('current_total_tax', 'FLOAT', 'NULLABLE'), SchemaField('taxes_included', 'BOOLEAN', 'NULLABLE'), SchemaField('processing_method', 'STRING', 'NULLABLE'), SchemaField('order_number', 'INTEGER', 'NULLABLE'), SchemaField('gateway', 'STRING', 'NULLABLE'), SchemaField('current_total_discounts', 'FLOAT', 'NULLABLE'), SchemaField('currency', 'STRING', 'NULLABLE'), SchemaField('current_subtotal_price', 'FLOAT', 'NULLABLE'), SchemaField('created_at', 'TIMESTAMP', 'NULLABLE'), 
SchemaField('cancelled_at', 'TIMESTAMP', 'NULLABLE'), SchemaField('admin_graphql_api_id', 'STRING', 'NULLABLE'), SchemaField('contact_email', 'STRING', 'NULLABLE'), SchemaField('cancel_reason', 'STRING', 'NULLABLE'), SchemaField('current_total_price', 'FLOAT', 'NULLABLE'), SchemaField('confirmed', 'BOOLEAN', 'NULLABLE'), SchemaField('total_discounts', 'FLOAT', 'NULLABLE')]



{'id': 4927012634690, 'order_id': 3946364043330, 'kind': 'sale', 'gateway': 'shopify_payments', 'status': 'failure',
    'message': 'The zip code you supplied failed validation.', 'created_at': '2021-09-06T04:42:50-05:00', 'source_name': '580111', 'amount': '27.50', 'currency': 'USD'}


transactions = [SchemaField('amount', 'FLOAT', 'NULLABLE'), SchemaField('currency', 'STRING', 'NULLABLE'), SchemaField('email', 'STRING', 'NULLABLE'), SchemaField('refunded', 'BOOLEAN', 'NULLABLE'), SchemaField('manual_entry', 'BOOLEAN', 'NULLABLE'), SchemaField('order_transaction_id', 'INTEGER', 'NULLABLE'), SchemaField('gateway', 'STRING', 'NULLABLE'), SchemaField('transaction_fee_tax_amount', 'INTEGER', 'NULLABLE'), SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField(
    'created_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('transaction_fee_total_amount', 'INTEGER', 'NULLABLE'), SchemaField('shop_name', 'STRING', 'NULLABLE'), SchemaField('source_name', 'STRING', 'NULLABLE'), SchemaField('payments_charge_id', 'INTEGER', 'NULLABLE'), SchemaField('kind', 'STRING', 'NULLABLE'), SchemaField('status', 'STRING', 'NULLABLE'), SchemaField('message', 'STRING', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE')]

order_risks = [SchemaField('merchant_message', 'STRING', 'NULLABLE'), SchemaField('cause_cancel', 'STRING', 'NULLABLE'), SchemaField('recommendation', 'STRING', 'NULLABLE'), SchemaField('display', 'BOOLEAN', 'NULLABLE'), SchemaField(
    'checkout_id', 'INTEGER', 'NULLABLE'), SchemaField('score', 'FLOAT', 'NULLABLE'), SchemaField('message', 'STRING', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('source', 'STRING', 'NULLABLE'), SchemaField('order_id', 'INTEGER', 'NULLABLE')]


shopify_discount_codes = [SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField('discount_codes_type', 'STRING', 'NULLABLE'), SchemaField('discount_codes_amount', 'FLOAT', 'NULLABLE'), SchemaField('discount_codes_code', 'STRING', 'NULLABLE')]

shopify_tax_lines = [SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField('tax_lines_title', 'STRING', 'NULLABLE'), SchemaField('tax_lines_rate', 'FLOAT', 'NULLABLE'), SchemaField('tax_lines_price', 'FLOAT', 'NULLABLE')]

shopify_line_items = [SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField('line_items_variant_title', 'STRING', 'NULLABLE'), SchemaField('line_items_total_discount', 'FLOAT', 'NULLABLE'), SchemaField('line_items_fulfillment_service', 'STRING', 'NULLABLE'), SchemaField('line_items_sku', 'STRING', 'NULLABLE'), SchemaField('line_items_product_exists', 'BOOLEAN', 'NULLABLE'), SchemaField('line_items_requires_shipping', 'BOOLEAN', 'NULLABLE'), SchemaField('line_items_origin_location_zip', 'INTEGER', 'NULLABLE'), SchemaField('line_items_variant_inventory_management', 'STRING', 'NULLABLE'), SchemaField('line_items_origin_location_province_code', 'STRING', 'NULLABLE'), SchemaField('line_items_vendor', 'STRING', 'NULLABLE'), SchemaField('line_items_variant_id', 'INTEGER', 'NULLABLE'), SchemaField('line_items_pre_tax_price', 'FLOAT', 'NULLABLE'), SchemaField('line_items_fulfillment_status', 'STRING', 'NULLABLE'), SchemaField('line_items_origin_location_country_code', 'STRING', 'NULLABLE'), SchemaField('line_items_origin_location_name', 'STRING', 'NULLABLE'), SchemaField('line_items_title', 'STRING', 'NULLABLE'), SchemaField('line_items_quantity', 'INTEGER', 'NULLABLE'), SchemaField('line_items_name', 'STRING', 'NULLABLE'), SchemaField('line_items_price', 'FLOAT', 'NULLABLE'), SchemaField('line_items_product_id', 'INTEGER', 'NULLABLE'), SchemaField('line_items_gift_card', 'BOOLEAN', 'NULLABLE'), SchemaField('line_items_taxable', 'BOOLEAN', 'NULLABLE'), SchemaField('line_items_origin_location_city', 'STRING', 'NULLABLE'), SchemaField('line_items_id', 'INTEGER', 'NULLABLE')]


shopify_shipping_lines = [SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField('shipping_lines_title', 'STRING', 'NULLABLE'), SchemaField('shipping_lines_source', 'STRING', 'NULLABLE')]


cretio_stast = [SchemaField('conversionrateclientattribution', 'FLOAT', 'NULLABLE'), 
SchemaField('advertisercost', 'FLOAT', 'NULLABLE'), SchemaField('salesallclientattribution', 'INTEGER', 'NULLABLE'), SchemaField('clicks', 'INTEGER', 'NULLABLE'), SchemaField('advertiser', 'STRING', 'NULLABLE'), SchemaField('day', 'DATE', 'NULLABLE'), SchemaField('roasallclientattribution', 'FLOAT', 'NULLABLE'), SchemaField('roasclientattribution', 'FLOAT', 'NULLABLE'), SchemaField('revenuegeneratedpc30d', 'FLOAT', 'NULLABLE'), SchemaField('revenuegeneratedallclientattribution', 'FLOAT', 'NULLABLE'), SchemaField('year', 'DATE', 'NULLABLE'), SchemaField('hour', 'TIMESTAMP', 'NULLABLE'), SchemaField('currency', 'STRING', 'NULLABLE'), SchemaField('os', 'STRING', 'NULLABLE'), SchemaField('month', 'DATE', 'NULLABLE'), SchemaField('salesclientattribution', 'INTEGER', 'NULLABLE'), SchemaField('displays', 'INTEGER', 'NULLABLE'), SchemaField('advertiserid', 'INTEGER', 'NULLABLE'), SchemaField('device', 'STRING', 'NULLABLE'), SchemaField('costperorderclientattribution', 'FLOAT', 'NULLABLE'), SchemaField('week', 'DATE', 'NULLABLE'), SchemaField('adsetid', 'INTEGER', 'NULLABLE'), SchemaField('category', 'FLOAT', 'NULLABLE'), SchemaField('adset', 'STRING', 'NULLABLE'), SchemaField('salespc30d', 'INTEGER', 'NULLABLE'), SchemaField('categoryid', 'INTEGER', 'NULLABLE')]


order_table = {
    "id": {},
    "admin_graphql_api_id": {},
    "cancel_reason": {},
    "cancelled_at": {},
    "confirmed": {},
    "contact_email": {},
    "created_at": {},
    "currency": {},
    "current_subtotal_price": {},
    "current_total_discounts": {},
    "current_total_price": {},
    "current_total_tax": {},
    "financial_status": {},
    "fulfillment_status": {},
    "gateway": {},
    "order_number": {},
    "processing_method": {},
    "source_name": {},
    "tags": {},
    "taxes_included": {

    },
    "total_discounts": {},
    "updated_at": {},
    "total_shipping_price_set": {
            "shop_money": {
                "amount": {

                }
            }
    },
    "shipping_address": {
        "city": {


        },

        "zip": {

        },

        "country": {

        },
         "province":{

    }

    },
    "shipping_lines":{
        "source":{},
        "title":{},
        "id":{},
        "code":{},
        "discounted_price":{},
        "price_set":{
        "presentment_money": {
            "amount":{}
        }
        },
        "price":{},
    },
    "line_items":{
        "id":{},
        "fulfillment_service":{},
        "fulfillment_status":{},
        "gift_card":{},
        "name":{},
        "origin_location":{
            "name":{},
            "country_code":{},
            "province_code":{},
            "city":{},
            "zip":{},
        },
        "pre_tax_price":{},
        "price":{},
        "product_exists":{},
        "product_id":{},
        "quantity":{},
        "requires_shipping":{},
        "sku":{},
        "taxable":{},
        "title":{},
        "total_discount":{},
        "variant_id":{},
        "variant_inventory_management":{},
        "variant_title":{},
        "vendor":{}
    },
    "discount_codes":{
        "code":{},
        "amount":{},
        "type":{}
    },
    "tax_lines":{
        "price":{},
        "rate":{},
        "title":{}
    }
}


order_refund_table = {
    "id":{},
    "order_id":{},
    "created_at":{},
    "user_id":{},
    "restock":{},
    "admin_graphql_api_id":{},
    "refund_line_items":{
        "id":{},
        "line_item_id":{},
        "restock_type":{},
        "subtotal":{},
        "total_tax":{},
        "line_item":{
            "variant_id":{},
            "title":{},
            "quantity":{},
            "sku":{},
            "variant_title":{},
            "vendor":{},
            "fulfillment_service":{},
            "product_id":{},
            "requires_shipping":{},
            "taxable":{},
            "name":{},
            "variant_inventory_management":{},
            "product_exists":{},
            "fulfillable_quantity":{},
            "price":{},
            "fulfillment_status":{}
        }
    }
    
}



products_table = {
    "id":{},
    "title":{},
    "vendor":{},
    "product_type":{},
    "created_at":{},
    "handle":{},
    "updated_at":{},
    "published_at":{},
    "template_suffix":{},
    "status":{},
    "published_scope":{},
    "tags":{},
    "admin_graphql_api_id":{}
}

product_variant_table = {
    "id":{},
    "product_id":{},
    "title":{},
    "sku":{},
    "position":{},
    "inventory_policy":{},
    "compare_at_price":{},
    "fulfillment_service":{},
    "inventory_management":{},
    "option1":{},
    "option2":{},
    "option3":{},
    "created_at":{},
    "updated_at":{},
    "taxable":{},
    "barcode":{},
    "grams":{},
    "weight":{},
    "weight_unit":{},
    "inventory_item_id":{},
    "inventory_quantity":{},
    "old_inventory_quantity":{},
    "tax_code":{},
    "requires_shipping":{},
    "admin_graphql_api_id":{}


}   






order_refunds = [SchemaField('admin_graphql_api_id', 'STRING', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('restock', 'BOOLEAN', 'NULLABLE'), SchemaField('user_id', 'INTEGER', 'NULLABLE'), SchemaField('created_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('order_id', 'INTEGER', 'NULLABLE')]


refund_line_items = [SchemaField('line_item_fulfillment_status', 'STRING', 'NULLABLE'), SchemaField('total_discount', 'FLOAT', 'NULLABLE'), SchemaField('line_item_product_exists', 'BOOLEAN', 'NULLABLE'), SchemaField('total_tax', 'FLOAT', 'NULLABLE'), SchemaField('line_item_taxable', 'BOOLEAN', 'NULLABLE'), SchemaField('line_item_price', 'FLOAT', 'NULLABLE'), SchemaField('line_item_fulfillable_quantity', 'INTEGER', 'NULLABLE'), SchemaField('gift_card', 'BOOLEAN', 'NULLABLE'), SchemaField('grams', 'INTEGER', 'NULLABLE'), SchemaField('line_item_fulfillment_service', 'STRING', 'NULLABLE'), SchemaField('refund_id', 'INTEGER', 'NULLABLE'), SchemaField('line_item_vendor', 'STRING', 'NULLABLE'), SchemaField('line_item_variant_title', 'STRING', 'NULLABLE'), SchemaField('line_item_title', 'STRING', 'NULLABLE'), SchemaField('line_item_requires_shipping', 'BOOLEAN', 'NULLABLE'), SchemaField('restock_type', 'STRING', 'NULLABLE'), SchemaField('line_item_sku', 'STRING', 'NULLABLE'), SchemaField('line_item_name', 'STRING', 'NULLABLE'), SchemaField('line_item_id', 'INTEGER', 'NULLABLE'), SchemaField('line_item_variant_id', 'INTEGER', 'NULLABLE'), SchemaField('line_item_variant_inventory_management', 'STRING', 'NULLABLE'), SchemaField('subtotal', 'FLOAT', 'NULLABLE'), SchemaField('line_item_quantity', 'INTEGER', 'NULLABLE'), SchemaField('line_item_product_id', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE')]



campaign_schema = [SchemaField('message_type', 'STRING', 'NULLABLE'), SchemaField('campaign_type', 'STRING', 'NULLABLE'), SchemaField('num_recipients', 'INTEGER', 'NULLABLE'), SchemaField('status_id', 'INTEGER', 'NULLABLE'), SchemaField('from_name', 'STRING', 'NULLABLE'), SchemaField('status', 'STRING', 'NULLABLE'), SchemaField('updated', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('object', 'STRING', 'NULLABLE'), SchemaField('send_time', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('template_id', 'STRING', 'NULLABLE'), SchemaField('is_segmented', 'BOOLEAN', 'NULLABLE'), SchemaField('created', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('from_email', 'STRING', 'NULLABLE'), SchemaField('sent_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('subject', 'STRING', 'NULLABLE'), SchemaField('status_label', 'STRING', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('id', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]

camp_list_schema = [SchemaField('person_count', 'INTEGER', 'NULLABLE'), SchemaField('camp_id', 'STRING', 'NULLABLE'), SchemaField('created', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('folder', 'STRING', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('id', 'STRING', 'NULLABLE'), SchemaField('list_type', 'STRING', 'NULLABLE'), SchemaField('updated', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('object', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]

camp_excluded_lists_schema = [SchemaField('person_count', 'INTEGER', 'NULLABLE'), SchemaField('camp_id', 'STRING', 'NULLABLE'), SchemaField('created', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('folder', 'STRING', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('id', 'STRING', 'NULLABLE'), SchemaField('list_type', 'STRING', 'NULLABLE'), SchemaField('updated', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('object', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]

camp_reciept = [SchemaField('camp_id', 'STRING', 'NULLABLE'), SchemaField('customer_id', 'STRING', 'NULLABLE'), SchemaField('variation_id', 'STRING', 'NULLABLE'), SchemaField('status', 'STRING', 'NULLABLE'), SchemaField('email', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]

metrics_table = {
    "object":{},
    "id":{},
    "name":{},
    "integration":{
        "object":{},
        "id":{},
        "name":{},
        "category":{}
    },
    "created":{},
    "updated":{}

}




metrics_timeline_table = {
    "object":{},
    "id":{},
    "statistic_id":{},
    "timestamp":{},
    "event_name":{},
    "event_properties":{
        "priority":{},
        "via":{
            "source":{
                "to":{},
                "from":{}
            },
            "channel":{}
        },
        "description":{},
        "tags":"Json_Save",
        "fields":"Json_Save",
        "group_name":{},
        "assignee_name":{},
        "ticket_id":{},
        "zendesk_url":{},
        "type":{},
        "Channel":{},
        "subject":{},
        "$value":{},
        "$event_id":{}
        
    },
    "person":{
        
            'object': {}, 
            'id': {}, 
            '$address1': {}, 
            '$address2': {}, 
            '$city': {},
            '$country': {}, 
            '$latitude': {}, 
            '$longitude': {}, 
            '$region': {}, 
            '$zip': {},
            '$organization': {},
            '$email': {},
            '$title': {},
            '$phone_number': {},
            '$first_name': {}, 
            '$last_name': {},
            '$timezone': {}, 
            '$id': {},
            'email': {},
            'first_name': {},
            'last_name': {},
            'created': {}, 
            'updated': {}
                   
    }

}


metrics = [SchemaField('created', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('integration_category', 'STRING', 'NULLABLE'), SchemaField('integration_id', 'STRING', 'NULLABLE'), SchemaField('integration_object', 'STRING', 'NULLABLE'), SchemaField('name', 'STRING', 'NULLABLE'), SchemaField('integration_name', 'STRING', 'NULLABLE'), SchemaField('id', 'STRING', 'NULLABLE'), SchemaField('updated', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('object', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]


klav_lists = [SchemaField('list_name', 'STRING', 'NULLABLE'), SchemaField('list_id', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]

metric_timeline = [SchemaField("object_type", "STRING","NULLABLE"),SchemaField("metric_id", "STRING","NULLABLE"),SchemaField('person_last_name', 'STRING', 'NULLABLE'), SchemaField('person_phone_number', 'STRING', 'NULLABLE'), SchemaField('person_title', 'STRING', 'NULLABLE'), SchemaField('person_email', 'STRING', 'NULLABLE'), SchemaField('person_first_name', 'STRING', 'NULLABLE'), SchemaField('person_organization', 'STRING', 'NULLABLE'), SchemaField('person_latitude', 'FLOAT', 'NULLABLE'), SchemaField('person_country', 'STRING', 'NULLABLE'), SchemaField('person_city', 'STRING', 'NULLABLE'), SchemaField('person_address2', 'STRING', 'NULLABLE'), SchemaField('person_zip', 'STRING', 'NULLABLE'), SchemaField('person_address1', 'STRING', 'NULLABLE'), SchemaField('person_created', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('datetime', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('event_properties_Channel', 'STRING', 'NULLABLE'), SchemaField('event_properties_value', 'FLOAT', 'NULLABLE'), SchemaField('person_longitude', 'FLOAT', 'NULLABLE'), SchemaField('person_object', 'STRING', 'NULLABLE'), SchemaField('event_properties_tags', 'STRING', 'NULLABLE'), SchemaField('event_properties_event_id', 'STRING', 'NULLABLE'), SchemaField('person_timezone', 'STRING', 'NULLABLE'), SchemaField('event_properties_type', 'STRING', 'NULLABLE'), SchemaField('event_properties_zendesk_url', 'STRING', 'NULLABLE'), SchemaField('event_properties_ticket_id', 'INTEGER', 'NULLABLE'), SchemaField('uuid', 'STRING', 'NULLABLE'), SchemaField('event_properties_subject', 'STRING', 'NULLABLE'), SchemaField('event_properties_assignee_name', 'STRING', 'NULLABLE'), SchemaField('person_updated', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('event_properties_group_name', 'STRING', 'NULLABLE'), SchemaField('event_properties_fields', 'STRING', 'NULLABLE'), SchemaField('event_properties_description', 'STRING', 'NULLABLE'), SchemaField('event_properties_via_channel', 'STRING', 'NULLABLE'), SchemaField('person_region', 'STRING', 'NULLABLE'), SchemaField('event_properties_priority', 'STRING', 'NULLABLE'), SchemaField('event_name', 'STRING', 'NULLABLE'), SchemaField('id', 'STRING', 'NULLABLE'), SchemaField('timestamp', 'INTEGER', 'NULLABLE'), SchemaField('object', 'STRING', 'NULLABLE'), SchemaField('statistic_id', 'STRING', 'NULLABLE'), SchemaField('person_id', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]


people_exclusions = [SchemaField('timestamp', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('reason', 'STRING', 'NULLABLE'), SchemaField('email', 'STRING', 'NULLABLE'), SchemaField('object', 'STRING', 'NULLABLE'),SchemaField("page_no", "INTEGER")]



product_schema = [SchemaField('tags', 'STRING', 'NULLABLE'), SchemaField('admin_graphql_api_id', 'STRING', 'NULLABLE'), SchemaField('title', 'STRING', 'NULLABLE'), SchemaField('published_scope', 'STRING', 'NULLABLE'), SchemaField('status', 'STRING', 'NULLABLE'), SchemaField('template_suffix', 'STRING', 'NULLABLE'), SchemaField('published_at', 'TIMESTAMP', 'NULLABLE'), SchemaField('updated_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('handle', 'STRING', 'NULLABLE'), SchemaField('product_type', 'STRING', 'NULLABLE'), SchemaField('created_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('vendor', 'STRING', 'NULLABLE')]

product_variant = [SchemaField('admin_graphql_api_id', 'STRING', 'NULLABLE'), SchemaField('requires_shipping', 'BOOLEAN', 'NULLABLE'), SchemaField('weight_unit', 'STRING', 'NULLABLE'), SchemaField('weight', 'FLOAT', 'NULLABLE'), SchemaField('taxable', 'BOOLEAN', 'NULLABLE'), SchemaField('grams', 'INTEGER', 'NULLABLE'), SchemaField('updated_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('inventory_item_id', 'INTEGER', 'NULLABLE'), SchemaField('barcode', 'STRING', 'NULLABLE'), SchemaField('fulfillment_service', 'STRING', 'NULLABLE'), SchemaField('created_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('option1', 'STRING', 'NULLABLE'), SchemaField('sku', 'STRING', 'NULLABLE'), SchemaField('inventory_management', 'STRING', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE'), SchemaField('compare_at_price', 'FLOAT', 'NULLABLE'), SchemaField('old_inventory_quantity', 'INTEGER', 'NULLABLE'), SchemaField('product_id', 'INTEGER', 'NULLABLE'), SchemaField('position', 'INTEGER', 'NULLABLE'), SchemaField('title', 'STRING', 'NULLABLE'), SchemaField('option3', 'STRING', 'NULLABLE'), SchemaField('inventory_policy', 'STRING', 'NULLABLE'), SchemaField('tax_code', 'STRING', 'NULLABLE'), SchemaField('inventory_quantity', 'INTEGER', 'NULLABLE'), SchemaField('option2', 'STRING', 'NULLABLE')]


disputed_table = {
    "id":{},
"order_id":{},
    "type":{},
    "amount":{},
    "currency":{},
    "reason":{},
    "network_reason_code":{},
    "status":{},
    "evidence_due_by":{},
    "evidence_sent_on":{},
    "finalized_on":{},
    "initiated_at":{}
}


disputes_schema = [SchemaField('finalized_on', 'TIMESTAMP', 'NULLABLE'), SchemaField('initiated_at', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('network_reason_code', 'STRING', 'NULLABLE'), SchemaField('evidence_due_by', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('reason', 'STRING', 'NULLABLE'), SchemaField('evidence_sent_on', 'TIMESTAMP', 'NULLABLE', 'bq-datetime'), SchemaField('status', 'STRING', 'NULLABLE'), SchemaField('currency', 'STRING', 'NULLABLE'), SchemaField('amount', 'FLOAT', 'NULLABLE'), SchemaField('type', 'STRING', 'NULLABLE'), SchemaField('order_id', 'INTEGER', 'NULLABLE'), SchemaField('id', 'INTEGER', 'NULLABLE')]


# order_table_another_table = {
#     "sho"
# }

uploaded_on = SchemaField("uploaded_on", "DATE")

agents_activity.append(uploaded_on)
incremental_calls.append(uploaded_on)
menu_routes.append(uploaded_on)
menus.append(uploaded_on)
voice_ivr.append(uploaded_on)
transactions.append(uploaded_on)
order_risks.append(uploaded_on)
shopify_discount_codes.append(uploaded_on)
shopify_tax_lines.append(uploaded_on)
shopify_line_items.append(uploaded_on)
shopify_shipping_lines.append(uploaded_on)
shopify_orders.append(uploaded_on)
cretio_stast.append(uploaded_on)
campaign_schema.append(uploaded_on)
camp_list_schema.append(uploaded_on)
camp_excluded_lists_schema.append(uploaded_on)
camp_reciept.append(uploaded_on)
metrics.append(uploaded_on)
klav_lists.append(uploaded_on)
metric_timeline.append(uploaded_on)
people_exclusions.append(uploaded_on)
order_refunds.append(uploaded_on)
refund_line_items.append(uploaded_on)
product_schema.append(uploaded_on)
product_variant.append(uploaded_on)
disputes_schema.append(uploaded_on)

schema["incremental_calls"] = incremental_calls
schema["agents_activity"] = agents_activity
schema["menu_routes"] = menu_routes
schema["menus"] = menus
schema["voice_ivr"] = voice_ivr
schema["orders"] = shopify_orders
schema["transactions"] = transactions
schema["order_risks"] = order_risks
schema["shopify_discount_codes"] = shopify_discount_codes
schema["shopify_tax_lines"] = shopify_tax_lines
schema["shopify_line_items"] = shopify_line_items
schema["shopify_shipping_lines"] = shopify_shipping_lines
schema["stastics"] = cretio_stast
schema["campaigns"] = campaign_schema
schema["camp_lists"] = camp_list_schema
schema["camp_excluded_lists"] = camp_excluded_lists_schema
schema["camp_reciept"] = camp_reciept
schema["metrics"] = metrics
schema["lists"] = klav_lists
schema["metrics_timelines"] = metric_timeline
schema["people_exclusions"] = people_exclusions
schema["order_refunds"] = order_refunds
schema["refund_line_items"] = refund_line_items
schema["product"] = product_schema
schema["product_variants"] = product_variant
schema["disputes"] = disputes_schema

conv_schema = {}

for key, values in schema.items():
    temp = []
    for sch in values:

        temp.append(sch.to_api_repr()["name"])
    conv_schema[key] = temp
