def db_sample_to_json(data_sample_list):
    out_json = []
    for sample in data_sample_list:
        out_json.append(
            {
                'id': sample.id,
                'disc': sample.disc,
                'theme': sample.theme,
                # 'text': sample.text,
                'date':sample.date,
                'username': sample.user_name 
            }
        )
    return out_json

def db_sample_to_json_text(sample):
    out_json = []
    
    out_json.append(
        {
            'id': sample.id,
            'disc': sample.disc,
            'theme': sample.theme,
            'text': sample.text,
            'date':sample.date,
            'username': sample.user_name 
        }
    )
    return out_json