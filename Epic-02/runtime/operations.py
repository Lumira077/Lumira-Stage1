def assess(feature,report):
    count=report.get('per_feature_tests',{}).get(feature,0)
    return {'feature':feature,'source_commit':report.get('source_commit'),'simulation_tests':count,
            'simulation_passed':report.get('passed') is True and count>0,
            'release_ready':False,'actual_participants':0,
            'pending':['real_model_and_hardware','actual_user_study','production_privacy_auth','rollback_and_Q1_R1_approval']}
