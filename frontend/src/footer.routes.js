// Material Kit 2 React components
import MKTypography from "components/MKTypography";

// // Images
import logoCT from "assets/images/logo-ct-dark.png";

const date = new Date().getFullYear();

// TODO footer routes
export default {
    brand: {
        name: "Booksearch",
        image: logoCT,
        route: "/",
    },
    socials: [],
    menus: [
        {
            name: "company",
            items: [
                { name: "about us", href: "https://www.creative-tim.com/presentation" },
                { name: "freebies", href: "https://www.creative-tim.com/templates/free" },
                { name: "premium tools", href: "https://www.creative-tim.com/templates/premium" },
                { name: "blog", href: "https://www.creative-tim.com/blog" },
            ],
        },
        {
            name: "resources",
            items: [
                { name: "illustrations", href: "https://iradesign.io/" },
                { name: "bits & snippets", href: "https://www.creative-tim.com/bits" },
                { name: "affiliate program", href: "https://www.creative-tim.com/affiliates/new" },
            ],
        },
        {
            name: "help & support",
            items: [
                { name: "contact us", href: "https://www.creative-tim.com/contact-us" },
                { name: "knowledge center", href: "https://www.creative-tim.com/knowledge-center" },
                { name: "custom development", href: "https://services.creative-tim.com/" },
                { name: "sponsorships", href: "https://www.creative-tim.com/sponsorships" },
            ],
        },
        {
            name: "legal",
            items: [
                { name: "terms & conditions", href: "https://www.creative-tim.com/terms" },
                { name: "privacy policy", href: "https://www.creative-tim.com/privacy" },
                { name: "licenses (EULA)", href: "https://www.creative-tim.com/license" },
            ],
        },
    ],
    copyright: (
        <MKTypography variant="button" fontWeight="regular">
            All rights reserved. Copyright &copy; {date} Material Kit by{" "}
            <MKTypography
                component="a"
                href="https://www.creative-tim.com"
                target="_blank"
                rel="noreferrer"
                variant="button"
                fontWeight="regular"
            >
                Creative Tim
            </MKTypography>
            .
        </MKTypography>
    ),
};
