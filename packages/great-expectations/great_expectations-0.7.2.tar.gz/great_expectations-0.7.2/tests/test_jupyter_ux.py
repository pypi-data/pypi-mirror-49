import great_expectations as ge
import great_expectations.jupyter_ux as jux
from great_expectations.profile.basic_dataset_profiler import BasicDatasetProfiler

def test_styling_elements_exist():
    assert "<link" in jux.bootstrap_link_element
    assert "bootstrap" in jux.bootstrap_link_element

    assert jux.cooltip_style_element[:23] == '<style type="text/css">'
    assert ".cooltip" in jux.cooltip_style_element

def test_display_column_expectations_as_section(basic_expectation_suite):
    html_to_display = jux.display_column_expectations_as_section(
        basic_expectation_suite,
        "naturals",
        include_styling=False,
        return_without_displaying=True
    )
    print(html_to_display)
    assert html_to_display == """\
<div id="section-1" class="ge-section container-fluid">
    <div class="row">
        
<div id="content-block-1" class="col-12" >
    <h3 id="content-block-1-header" class="alert alert-secondary" >
        naturals
    </h3>
</div>
        
<div id="content-block-2" class="col-12" >
    <ul id="content-block-2-body" >
            <li >is a required field.</li>
            <li >values must be unique.</li>
            
        </ul>
</div>
        
    </div>
</div>"""

    html_to_display = jux.display_column_expectations_as_section(
        basic_expectation_suite,
        "naturals",
        return_without_displaying=True
    )
    print(html_to_display)
    assert html_to_display == """\
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><style type="text/css">
.cooltip {
    display:inline-block;
    position:relative;
    text-align:left;
}

.cooltip .top {
    min-width:200px; 
    top:-6px;
    left:50%;
    transform:translate(-50%, -100%);
    padding:10px 20px;
    color:#FFFFFF;
    background-color:#222222;
    font-weight:normal;
    font-size:13px;
    border-radius:8px;
    position:absolute;
    z-index:99999999;
    box-sizing:border-box;
    box-shadow:0 1px 8px rgba(0,0,0,0.5);
    display:none;
}

.cooltip:hover .top {
    display:block;
}

.cooltip .top i {
    position:absolute;
    top:100%;
    left:50%;
    margin-left:-12px;
    width:24px;
    height:12px;
    overflow:hidden;
}

.cooltip .top i::after {
    content:'';
    position:absolute;
    width:12px;
    height:12px;
    left:50%;
    transform:translate(-50%,-50%) rotate(45deg);
    background-color:#222222;
    box-shadow:0 1px 8px rgba(0,0,0,0.5);
}
</style>
<div id="section-1" class="ge-section container-fluid">
    <div class="row">
        
<div id="content-block-1" class="col-12" >
    <h3 id="content-block-1-header" class="alert alert-secondary" >
        naturals
    </h3>
</div>
        
<div id="content-block-2" class="col-12" >
    <ul id="content-block-2-body" >
            <li >is a required field.</li>
            <li >values must be unique.</li>
            
        </ul>
</div>
        
    </div>
</div>"""

def test_display_column_evrs_as_section():
    #TODO: We should add a fixture that contains EVRs
    df = ge.read_csv("./tests/test_sets/Titanic.csv")
    df.profile(BasicDatasetProfiler)
    evrs = df.validate(result_format="SUMMARY")  # ["results"]

    html_to_display = jux.display_column_evrs_as_section(
        evrs,
        "Name",
        include_styling=False,
        return_without_displaying=True
    )
    print(html_to_display)

    #FIXME: This isn't a full snapshot test.
    assert '<div id="section-1" class="ge-section container-fluid">' in html_to_display
    assert '<span class="badge badge-info" >Carlsson, Mr Frans Olof</span>' in html_to_display
    assert '<li class="list-group-item d-flex justify-content-between align-items-center" >expect_column_values_to_be_in_type_list <span class="badge badge-secondary badge-pill" >True</span></li>' in html_to_display
