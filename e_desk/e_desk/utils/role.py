import frappe
import json

@frappe.whitelist()
def update_user_role(user, role_name):
    user.update({
        "role_profile_name": role_name,
        "user_type": "System User"
    })
    user.save()
    frappe.db.commit()
@frappe.whitelist()
def update_event_participant_role(participant,confer, role_name):
    event_participant= frappe.db.get_value('Event Participant', {'parent': confer,'participant':participant}, ['name'])
    frappe.db.set_value('Event Participant', event_participant, 'event_role', role_name, update_modified=False)
    user=frappe.get_doc('User',{'participant_id': participant})
    update_user_role(user ,role_name)

@frappe.whitelist()
def get_filtered_confer(doctype, txt, searchfield, start, page_len,filters):
    participant = filters.get('participant')
    # Query to get Confer records where the Event Participant has the specific participant
    conf = frappe.db.sql(
        """
        SELECT c.name
        FROM `tabConfer` AS c
        JOIN `tabEvent Participant` AS ep ON c.name = ep.parent
        WHERE ep.participant = %(participant)s
        """,
        {
            'participant': participant
        }
    )
    
    return conf
