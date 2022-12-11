// Material Kit 2 React components
import MKTypography from "components/MKTypography";

// // Images
import logoCT from "assets/images/logo-ct-dark.png";

const date = new Date().getFullYear();

export default {
    brand: {
        name: "Booksearch",
        image: logoCT,
        route: "/",
    },
    socials: [],
    menus: [],
    copyright: (
        <MKTypography variant="button" fontWeight="regular">
            All rights reserved. Copyright &copy; {date} Booksearch by Group 68 of PRI class @ FEUP.
        </MKTypography>
    ),
};
