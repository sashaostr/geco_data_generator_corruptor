import os
import sys
import csv
import time
import unittest
import traceback
sys.path.append('..')

# Import data generator modules required
#
from geco_data_generator_corruptor import attrgenfunct
from geco_data_generator_corruptor import contdepfunct
from geco_data_generator_corruptor import basefunctions
from geco_data_generator_corruptor import generator
from geco_data_generator_corruptor import corruptor

import pkg_resources as pr


import random

random.seed(42)  # Set seed for random generator
unicode_encoding_used = 'ascii'

num_org_rec = 5

################################### Latent data generator ################################################


attr_data_list_extended = [{'generator': generator.GenerateFreqAttribute(attribute_name = 'first_name',
                                                                        freq_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','givenname_freq.csv'),
                                                                        has_header_line = False,
                                                                        unicode_encoding = unicode_encoding_used),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                           {'generator':generator.GenerateFreqAttribute(attribute_name = 'last_name',
                                                                        freq_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','surname-freq.csv'),
                                                                        has_header_line = False,
                                                                        unicode_encoding = unicode_encoding_used),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                           {'generator':generator.GenerateFuncAttribute(attribute_name = 'id',
                                                                        function=attrgenfunct.generate_social_id,
                                                                        parameters=[9]),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                           {'generator':generator.GenerateFuncAttribute(attribute_name = 'email',
                                                                        function=attrgenfunct.generate_email_address,
                                                                        parameters=[10]),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                            {'generator':generator.GenerateFuncAttribute(attribute_name = 'phone',
                                                                         function=attrgenfunct.generate_phone_number_australia),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                            {'generator':generator.GenerateFreqAttribute(attribute_name = 'product',
                                                                        freq_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','product_freq.csv'),
                                                                        has_header_line = False,
                                                                        unicode_encoding = unicode_encoding_used),
                            'data_type': 'ShortString',
                            'has_missing': True
                            },
                ]

attr_data_list = map(lambda s: s['generator'], attr_data_list_extended)
attr_name_list = map(lambda s: s.attribute_name, attr_data_list)
attr_metadata = map(lambda s: {'field': s['generator'].attribute_name,
                                  'has_missing': s['has_missing'],
                                  'type': s['data_type']},
                       attr_data_list_extended)

test_data_generator = generator.GenerateDataSet(\
                        output_file_name = 'no-file-name',
                        write_header_line = True,
                        rec_id_attr_name = 'rec_id',
                        number_of_records = num_org_rec,
                        attribute_name_list = attr_name_list,
                        attribute_data_list = attr_data_list,
                        unicode_encoding = unicode_encoding_used)

################################### corruptor ################################################


nothing_corruptor = corruptor.CorruptNothing()

average_edit_corruptor = corruptor.CorruptValueEdit(position_function = corruptor.position_mod_normal,
                                                   char_set_funct = basefunctions.char_set_ascii,
                                                   insert_prob = 0.25,
                                                   delete_prob = 0.25,
                                                   substitute_prob = 0.25,
                                                   transpose_prob = 0.25)

sub_tra_edit_corruptor = corruptor.CorruptValueEdit(position_function = corruptor.position_mod_uniform,
                                                   char_set_funct = basefunctions.char_set_ascii,
                                                   insert_prob = 0.0,
                                                   delete_prob = 0.0,
                                                   substitute_prob = 0.5,
                                                   transpose_prob = 0.5)

ins_del_edit_corruptor = corruptor.CorruptValueEdit(position_function = corruptor.position_mod_normal,
                                                   char_set_funct = basefunctions.char_set_ascii,
                                                   insert_prob = 0.5,
                                                   delete_prob = 0.5,
                                                   substitute_prob = 0.0,
                                                   transpose_prob = 0.0)

last_name_misspell_corruptor = corruptor.CorruptCategoricalValue(lookup_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','surname-misspell.csv'),
                                                               has_header_line = False,
                                                               unicode_encoding = unicode_encoding_used)

ocr_corruptor = corruptor.CorruptValueOCR(position_function = corruptor.position_mod_uniform,
                                       lookup_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','ocr-variations.csv'),
                                       has_header_line = False,
                                       unicode_encoding = unicode_encoding_used)

keyboard_corruptor = corruptor.CorruptValueKeyboard(position_function = corruptor.position_mod_normal,
                                                   row_prob = 0.5,
                                                   col_prob = 0.5)

phonetic_corruptor = corruptor.CorruptValuePhonetic(position_function = corruptor.position_mod_uniform,
                                                   lookup_file_name = pr.resource_filename('geco_data_generator_corruptor.lookup-files','phonetic-variations.csv'),
                                                   has_header_line = False,
                                                   unicode_encoding = unicode_encoding_used)

missing_val_empty_corruptor = corruptor.CorruptMissingValue()
missing_val_miss_corruptor = corruptor.CorruptMissingValue(missing_value='miss')
missing_val_unkown_corruptor = corruptor.CorruptMissingValue(missing_value='unknown')


################################### CRM corruptor ################################################



# For each attribute, a distribution of which corruptors to apply needs
# to be given, with the sum ofprobabilities to be 1.0 for each attribute
#
crm_attr_mod_prob_dictionary = {'first_name':0.2,
                                'last_name':0.2,
                                'id':0.05,
                                'email':0.55
                                }

crm_attr_mod_data_dictionary = \
  {'first_name':[(0.1, average_edit_corruptor),
                 (0.1, ocr_corruptor),
                 (0.1, phonetic_corruptor)],
   'last_name':[(0.1, last_name_misspell_corruptor),
              (0.1, average_edit_corruptor)],
   'id':[(0.3, sub_tra_edit_corruptor)],
   'email':[(0.1, average_edit_corruptor),
            (0.1, ocr_corruptor),
            (0.1, phonetic_corruptor),
            (0.5, missing_val_empty_corruptor)]}


# Initialise the main data corruptor
crm_data_corruptor = corruptor.CorruptDataSet(\
                        number_of_org_records = num_org_rec,
                        number_of_mod_records = num_org_rec,
                        attribute_name_list = attr_name_list,
                        max_num_dup_per_rec = 1,
                        num_dup_dist = 'uniform',
                        max_num_mod_per_attr = 1,
                        num_mod_per_rec = 1,
                        attr_mod_prob_dict = crm_attr_mod_prob_dictionary,
                        attr_mod_data_dict = crm_attr_mod_data_dictionary)

################################### EMAIL corruptor ################################################

#
email_attr_mod_prob_dictionary = {'first_name':0.05,
                                 'last_name':0.1,
                                 'id':0.3,
                                 'phone':0.275,
                                 'product':0.275
                                }

email_attr_mod_data_dictionary = \
                      {'first_name':[(0.3, average_edit_corruptor),
                                     (0.1, ocr_corruptor),
                                     (0.1, phonetic_corruptor),
                                     (0.5, missing_val_empty_corruptor)],
                      'last_name':[(0.3, average_edit_corruptor),
                                   (0.1, ocr_corruptor),
                                   (0.1, phonetic_corruptor),
                                   (0.5, missing_val_empty_corruptor)],
                      'id':[(0.1, sub_tra_edit_corruptor),
                            (0.9, missing_val_empty_corruptor)],
                      'phone':[(0.1, sub_tra_edit_corruptor),
                             (0.9, missing_val_empty_corruptor)],
                      'product':[(0.1, sub_tra_edit_corruptor),
                             (0.9, missing_val_empty_corruptor)],
                       }

# Initialise the main data corruptor
email_data_corruptor = corruptor.CorruptDataSet(\
                        number_of_org_records = num_org_rec,
                        number_of_mod_records = num_org_rec*5,
                        attribute_name_list = attr_name_list,
                        max_num_dup_per_rec = 10,
                        num_dup_dist = 'poisson',
                        max_num_mod_per_attr = 2,
                        num_mod_per_rec = 4,
                        attr_mod_prob_dict = email_attr_mod_prob_dictionary,
                        attr_mod_data_dict = email_attr_mod_data_dictionary)


try:
    rec_dict = test_data_generator.generate()
    print rec_dict

    crm_rec_dict = crm_data_corruptor.corrupt_records(rec_dict.copy())
    print crm_rec_dict

    email_rec_dict = email_data_corruptor.corrupt_records(rec_dict.copy())
    print email_rec_dict



    def dick_to_rec(dic):
        dups = filter(lambda kv: 'org' not in kv[0], dic.items())
        rows = map(lambda kv: [kv[0].split('-')[1]] + kv[1], dups)
        return rows

    def write_to_csv_file(records, header=None, file_name='output'):
        with open(file_name+'.csv', "wb") as f:
            writer = csv.writer(f)
            if header:
                writer.writerows([header])
            if records:
                writer.writerows(records)

    def write_to_file(records, header=None, file_name='output'):
        with open(file_name, "wb") as f:
            if header:
                f.write([header])
            if records:
                # f.writelines(map(lambda r: str(r)+'\n', records))
                f.write(str(records))




    crm_rec = dick_to_rec(crm_rec_dict)
    email_rec = dick_to_rec(email_rec_dict)


    rec_header = ['latent_id'] + attr_name_list
    write_to_csv_file(crm_rec, rec_header, 'output/crm')
    write_to_csv_file(email_rec, rec_header, 'output/email')

    write_to_file(attr_metadata, file_name='output/crm_email.metadata')


    # print 'generate records: %s' % len(rec_dict)

except Exception as exce_value:  # Something bad happened
    print 'generator.generate() raised Exception: "%s"' % str(exce_value)
    tb = traceback.format_exc()
    print tb



