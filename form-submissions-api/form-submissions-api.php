<?php
/**
* Plugin Name: Form Submission API
* Version: 3
* Description: This plugin creates table user_stories and registers http endpoints.
* Author: John G Schwitz
* Author URI: https://nebula-nlp.com
* Used Wordpress Plugin Dev: 
* https://learn.wordpress.org/tutorial/wordpress-rest-api-custom-routes-endpoints/
* NEEDED to add THIS add_action( 'rest_api_init', 'register_routes' )
**/

register_activation_hook( __FILE__, 'setup_table' );

/*
added because error undefined function wp_get_current_user() 
if(!function_exists('wp_get_current_user')) {
    include(ABSPATH . "wp-includes/pluggable.php"); 
}
*/

function setup_table() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'user_stories';

    $sql = "CREATE TABLE $table_name (
        story_id int(11) NOT NULL AUTO_INCREMENT,
        user_id int(11) NOT NULL,
        story_name char(50) NOT NULL,
        story mediumtext NOT NULL,
        PRIMARY KEY (`story_id`)
    )";

    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
    dbDelta( $sql );
}

/**
 * Register the REST API form-submissions-api/v2/form-submission routes
 */
add_action( 'rest_api_init', 'register_routes' );
function register_routes() {
    // Register the routes

    // Retrieve ALL form submissions
    register_rest_route(
        'form-submissions-api/v2',
        '/form-submissions/',
        array(
            'methods'  => 'GET',
            'callback' => 'get_form_submissions',
            'permission_callback' => '__return_true'
        )
    );
}

/**
 * GET callback for the form-submissions-api/v2/form-submission route
*
* @return array|object|stdClass[]|null
*/
function get_form_submissions() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'user_stories';

    $results = $wpdb->get_results( "SELECT * FROM $table_name" );

    return $results;
}

/**
 * POST add_action('rest_api_init, ) WAS NEEDED TO MAKE THIS WORK
 */
add_action('rest_api_init', function() {
    register_rest_route(        
        'form-submissions-api/v2',
        '/form-submission/',
         array(
            'methods'  => 'POST',
            'callback' => 'create_form_submission',
            'permission_callback' => '__return_true'
    ));
});


/**
 * POST callback for the wp-learn-form-submissions-api/v1/form-submission route
 *
 * @param $request
 *
 * @return void
 */
function create_form_submission( $request ){
    global $wpdb;
    $table_name = $wpdb->prefix . 'user_stories';
    
    $rows = $wpdb->insert(
        $table_name,
        array(
            'story_id' => $request['story_id'],
            'user_id' => $request['user_id'],
            'story_name' => $request['story_name'],
            'story' => $request['story'],
        )
    );

    return $rows;
}

/**
 * GET single
 */
add_action('rest_api_init', function() {
    register_rest_route(
        'form-submissions-api/v2',
        '/form-submission/(?P<id>\d+)',
        array(
            'methods'  => 'GET',
            'callback' => 'rest_get_form_submission',
            'permission_callback' => '__return_true'
        ));
});

function rest_get_form_submission( $request ) {
    $id = $request['user_id'];
    global $wpdb;
    $table_name = $wpdb->prefix . 'user_stories';

    $results = $wpdb->get_results( "SELECT * FROM $table_name WHERE id = $id" );

    return $results[0];
}

/**
 * Register the REST API asyn-function-api/v2/pdf-download route
 * Will use POST with $request
 */
add_action('rest_api_init', function() {
    register_rest_route(        
        'asyn-function-api/v2',
        '/pdf-download/',
         array(
            'methods'  => 'POST',
            'callback' => 'create_pdf_download',
            'permission_callback' => '__return_true'
    ));
});

/**
 * POST callback for asyn-function-api/v2/pdf-download route
 *
 * @param $request
 *
 * @return void
 */
function create_pdf_download( $request ){

    //var_dump($_REQUEST);  THIS WORKS TO DUMP VARIABLES IN ARRAY

    $bce2 = $request['story'];  // YES THIS WORKS
    // var_dump( $bce2);  // YES THIS WORKS
 
    $ace2 = $request['story_name'];
    //$user_ID = get_current_user_id(); 
    
    // Include the main TCPDF library (search for installation path).
    //require_once('config/tcpdf_config.php');
    require('tcpdf.php');

    // Extend the TCPDF class to create custom Header and Footer
    class MYPDF extends TCPDF {
    
        public function Header() {
            // 2) ADDED TITLE
            // Set font
            $this->setFont('caveat-bold', '', 24);
            // Title
            $this->Cell(0, 20, "Story Generated using Google Gemini", 0, 1, 'C', 0, '', 0, false, 'C', 'M');
            // THIS WORKS
            //$this->Multicell(0,20,"Story Generated using Google Gemini\n", 0, 'C'); 
            // WEB SITE
            $this->setFont('times', '', 8); 
            $html='<h1><a href="https://nebula-nlp.com">Nebula-NLP.com</a></h1>';
            $this->writeHTML($html, true, false, true, false, 'L');
        }
        
        // Page footer
        public function Footer() {
            // Position at 15 mm from bottom
            $this->SetY(-15);
            // Set font
            $this->SetFont('times', 'I', 8);
            // Page number
            $this->Cell(0, 10, 'Page '.$this->getAliasNumPage(), 0, false, 'C', 0, '', 0, false, 'T', 'M');
        }
    }
    // create new PDF document
    $pdf = new MYPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);

    // set default header data
    $pdf->SetHeaderData(PDF_HEADER_LOGO, PDF_HEADER_LOGO_WIDTH, PDF_HEADER_TITLE, PDF_HEADER_STRING);

    // set header and footer fonts
    $pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
    $pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

    // set default monospaced font
    $pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

    // set margins
    $pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
    $pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
    $pdf->SetFooterMargin(PDF_MARGIN_FOOTER);

    // set auto page breaks
    $pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

    // set font
    $pdf->SetFont('times', 'BI', 12);

    // add a page
    $pdf->AddPage();
    
    // 3) STORY NAME
    // Set font
    $pdf->setFont('caveat-bold', '', 18);
    // Title
    $pdf->Cell(70, 20, 'Story Name:', 0, 0, 'R', 0, '', 0, false, 'C', 'M');
    // 4) SUBMITTED TITLE
    $TITLE = 'Fearless Princess Hazel';
    // Set font
    $pdf->setFont('caveat-bold', '', 16);
    // Title
    $pdf->Cell(0, 0, $ace2, 0, 0, 'L', 0, '', 0, false, 'C', 'M');

    // print a block of text using Write()
    //var_dump($bce2);  //YES WORKING !!!!!!!!!! PERFECT PERFECT
    $pdf->setFont('times', 'BI', 12);
    $pdf->MultiCell(0, 10, $bce2, 0, 'L');  // BOTH ARE NEEDED TO GET OUTPUT ?????????????
    $pdf->Write(10, $bce2, '', 0, '',false, 0, false, false, 0);
    //Close and output PDF document
    $pdf->Output('GeneratedStory.pdf','I');

};

?>
