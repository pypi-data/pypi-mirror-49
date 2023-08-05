# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from nose.tools import assert_raises

testdir = os.path.dirname(os.path.realpath(__file__))
mock_pairsam_path = os.path.join(testdir, 'data', 'mock.pairsam')
mock_chromsizes_path = os.path.join(testdir, 'data', 'mock.chrom.sizes')


def test_preserve():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             'True',
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e

        
    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]
    assert all(l in pairsam_body for l in output_body)


def test_equal():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             '(pair_type == "RU") or (pair_type == "UR") or (pair_type == "UU")',
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e
    print(result)

    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]

    assert all(l.split('\t')[7] in ['RU', 'UR', 'UU'] for l in output_body)
    assert all(l in output_body
               for l in pairsam_body 
               if l.split('\t')[7] in ['RU', 'UR', 'UU'])


def test_csv():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             'csv_match(pair_type, "RU,UR,UU")',
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e
    print(result)

    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]

    assert all(l.split('\t')[7] in ['RU','UR', 'UU'] for l in output_body)
    assert all(l in output_body
               for l in pairsam_body 
               if l.split('\t')[7] in ['RU', 'UR', 'UU'])


def test_wildcard():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             'wildcard_match(pair_type, "*U")',
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e
    print(result)

    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]

    assert all(l.split('\t')[7] in ['NU', 'MU', 'RU', 'UU'] for l in output_body)
    assert all(l in output_body
               for l in pairsam_body 
               if l.split('\t')[7] in ['NU', 'MU', 'RU', 'UU'])


def test_regex():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             'regex_match(pair_type, "[NM]U")',
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e
    print(result)

    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]

    assert all(l.split('\t')[7] in ['NU', 'MU'] for l in output_body)
    assert all(l in output_body
               for l in pairsam_body 
               if l.split('\t')[7] in ['NU', 'MU'])
    
def test_chrom_subset():
    try:
        result = subprocess.check_output(
            ['python',
             '-m',
             'pairtools',
             'select',
             'True',
             '--chrom-subset',
             mock_chromsizes_path,
             mock_pairsam_path],
            ).decode('ascii')
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(sys.exc_info())
        raise e

        
    pairsam_body = [l.strip() for l in open(mock_pairsam_path, 'r') 
                    if not l.startswith('#') and l.strip()]
    output_body  = [l.strip() for l in result.split('\n')
                    if not l.startswith('#') and l.strip()]
    output_header = [l.strip() for l in result.split('\n')
                    if l.startswith('#') and l.strip()]

    chroms_from_chrom_field = [l.strip().split()[1:]
                               for l in result.split('\n')
                               if l.startswith('#chromosomes:')][0]

    assert set(chroms_from_chrom_field) == set(['chr1', 'chr2'])

    chroms_from_chrom_sizes = [l.strip().split()[1]
                               for l in result.split('\n')
                               if l.startswith('#chromsize:')]

    assert set(chroms_from_chrom_sizes) == set(['chr1', 'chr2'])
