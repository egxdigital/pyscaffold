import pytest
from pyscaffold.arg_parser import create_parser

def test_version_option(capsys):
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--version'])
    captured = capsys.readouterr()
    assert 'pyscaffold 1.0.0' in captured.out

def test_list_command():
    parser = create_parser()
    args = parser.parse_args(['list', '--destination', 'some/directory'])
    assert args.command == 'list'
    assert args.destination == 'some/directory'

def test_start_command():
    parser = create_parser()
    args = parser.parse_args(['start', 'ProjectA', 'ProjectB', '--destination', 'some/other/directory'])
    assert args.command == 'start'
    assert args.project_names == ['ProjectA', 'ProjectB']
    assert args.destination == 'some/other/directory'

def test_resume_command():
    parser = create_parser()
    args = parser.parse_args(['resume', 'ProjectA', '--destination', 'yet/another/directory'])
    assert args.command == 'resume'
    assert args.project_name == 'ProjectA'
    assert args.destination == 'yet/another/directory'

def test_no_command():
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_help_option(capsys):
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--help'])
    captured = capsys.readouterr()
    assert 'usage:' in captured.out
