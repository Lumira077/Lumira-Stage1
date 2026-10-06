"""Explicitly simulated device, profile context and output contracts."""
from .core import Error, require

class SimulatedDevice:
    mode = 'simulated'
    hardware_connected = False
    def __init__(self):
        self.devices = {
            'demo-device-01': {'owner':'local-demo-owner', 'connected':True},
            'demo-guardian-01': {'owner':'local-demo-guardian', 'connected':True},
            'demo-guest-01': {'owner':'local-demo-owner', 'connected':True},
        }
    def inspect(self, actor, device):
        d = self.devices.get(device)
        require(d is not None and d['owner'] == actor, 'DEVICE_NOT_AUTHORIZED', 403)
        return {'device_id':device,'connected':d['connected'],'adapter_mode':self.mode,
                'hardware_connected':False,'ownership_verified':'simulation_fixture'}
    def ready(self, actor, device):
        d = self.inspect(actor, device)
        require(d['connected'], 'DEVICE_DISCONNECTED', 409)
        return d
    def set_connected(self, actor, device, value):
        require(type(value) is bool, 'INVALID_INPUT')
        self.inspect(actor, device)
        self.devices[device]['connected'] = value
        return self.inspect(actor, device)

class ProfileAdapter:
    contract_version = 'f2002-minimal-v1'
    def context(self, profile_id, actor, draft):
        guest = draft['registration']['registration_type'] == 'guest'
        return {'contract_version':self.contract_version,'profile_id':profile_id,
                'actor_id':actor,'subject_id':draft['registration']['subject_id'],
                'registration_type':draft['registration']['registration_type'],
                'language':draft['language']['language'],**draft['profile'],
                'purpose':draft['purpose']['purpose'],'preferences':draft['preferences'],
                'permissions':{k:(False if guest else draft['consent'][k]) for k in
                               ('long_term_memory','conversation_storage','biometric_identity','cloud_transfer')},
                'policy_version':draft['consent']['policy_version'],
                'adapter_mode':'simulated','hardware_connected':False}

class SimulatedOutputs:
    modules = ('context', 'tts', 'expression', 'motion')
    def __init__(self, fail_once=None):
        self.fail_once = fail_once
    def apply(self, application_id, module, context):
        if self.fail_once == module:
            self.fail_once = None
            raise RuntimeError('simulated module failure')
        # No physical output. Motion never receives an actuator command here.
        return {'application_id':application_id,'module':module,'ack':True,
                'adapter_mode':'simulated','hardware_connected':False,
                'physical_action_performed':False}
    def greeting(self, context):
        if context['language'] == 'en-US':
            text = f"Hello, {context['preferred_name']}. I am Lumira. Is this voice and speaking speed comfortable?"
        else:
            text = f"{context['preferred_name']}, 안녕하세요. 저는 루미라입니다. 지금 목소리와 말하는 속도가 괜찮으세요?"
        return {'text':text,'preferences':context['preferences'],'adapter_mode':'simulated',
                'hardware_connected':False,'robot_audio_played':False}
