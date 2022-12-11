/*
=========================================================
* Material Kit 2 React - v2.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-kit-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// prop-types is a library for typechecking of props.
import PropTypes from "prop-types";

// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";

function DefaultFooter({ content }) {
    const { copyright } = content;

    return (
        <MKBox component="footer">
            <Container>
                <Grid container spacing={3}>
                    <Grid item xs={12} sx={{ textAlign: "center", my: 3 }}>
                        {copyright}
                    </Grid>
                </Grid>
            </Container>
        </MKBox>
    );
}

// Typechecking props for the DefaultFooter
DefaultFooter.propTypes = {
    content: PropTypes.objectOf(PropTypes.oneOfType([PropTypes.object, PropTypes.array]))
        .isRequired,
};

export default DefaultFooter;
