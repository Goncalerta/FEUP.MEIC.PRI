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

// @mui material components
import Container from "@mui/material/Container";
import Card from "@mui/material/Card";

// Material Kit 2 React components
import MKBox from "components/MKBox";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";
import DefaultFooter from "examples/Footers/DefaultFooter";
import { useEffect, useRef, useState } from "react";
import AdvancedSearch from "booksearch/AdvancedSearch/AdvancedSearch";

// Routes
import routes from "routes";
import footerRoutes from "footer.routes";
import api from "api";
// Images
import bgImage from "assets/images/bg-presentation.jpg";
import SearchResults from "booksearch/SearchResults/SearchResults";

function Presentation() {
    const [searchResults, setSearchResults] = useState({
        first_load: true,
        loading: true,
        data: {},
        error: false,
    });

    const resultsRef = useRef(null);

    const onSearch = (data) => {
        setSearchResults({ first_load: false, loading: false, data, error: false });
        resultsRef.current.scrollIntoView();
    };

    const onError = () => {
        setSearchResults({ first_load: false, loading: false, data: {}, error: true });
    };

    const onStartSearch = () => {
        setSearchResults({ first_load: false, loading: true, data: {}, error: false });
    };

    const exactSearch = async (query) => {
        console.log(query);
        onStartSearch();
        api.get("search", {
            params: {
                value: query.orig_query,
                exact_query: true,
                // TODO advanced search fields
            },
        })
            .then((response) => {
                onSearch(response.data);
            })
            .catch((e) => {
                console.log("Error", e);
                onError();
            });
    };

    const browse = async () => {
        try {
            const response = await api.get("browse", { page: 0 });
            if (searchResults.first_load) {
                if (response.status === 200) {
                    setSearchResults({
                        first_load: false,
                        loading: false,
                        data: response.data,
                        error: false,
                    });
                } else {
                    setSearchResults({ first_load: false, loading: false, data: [], error: true });
                }
            }
        } catch (e) {
            if (searchResults.first_load) {
                setSearchResults({ first_load: false, loading: false, data: [], error: true });
            }
        }
    };

    useEffect(() => browse(), []);

    return (
        <>
            <DefaultNavbar routes={routes} sticky />
            <MKBox
                minHeight="75vh"
                width="100%"
                sx={{
                    backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.75)),url(${bgImage})`,
                    backgroundSize: "cover",
                    backgroundPosition: "top",
                    display: "grid",
                    placeItems: "center",
                }}
            >
                <Container>
                    <AdvancedSearch
                        onSearch={onSearch}
                        onError={onError}
                        onStartSearch={onStartSearch}
                    />
                </Container>
            </MKBox>
            <Card
                sx={{
                    p: 2,
                    mx: { xs: 2, lg: 3 },
                    mt: -8,
                    mb: 4,
                    backgroundColor: ({ palette: { white }, functions: { rgba } }) =>
                        rgba(white.main, 0.8),
                    backdropFilter: "saturate(200%) blur(30px)",
                    boxShadow: ({ boxShadows: { xxl } }) => xxl,
                }}
            >
                <div ref={resultsRef} />
                <SearchResults
                    data={searchResults.data}
                    loading={searchResults.loading}
                    error={searchResults.error}
                    exactSearch={exactSearch}
                />
            </Card>
            <MKBox pt={6} px={1} mt={6}>
                <DefaultFooter content={footerRoutes} />
            </MKBox>
        </>
    );
}

export default Presentation;
