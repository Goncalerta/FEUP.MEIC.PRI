/* eslint-disable */

import { Box, CircularProgress, Container, Rating, Typography } from "@mui/material";
import PropTypes from "prop-types";
import StarIcon from "@mui/icons-material/Star";
import dayjs from "dayjs";
import MKButton from "components/MKButton";

function SearchResults(props) {
    const { loading, error, data, moreLikeThis } = props;

    const ERROR_MESSAGE = "An error occurred  while fetching results :(";
    const NO_RESULTS_MESSAGE = "No results found.";

    const authorsToText = (authors) => {
        let val = authors || [];
        if (!Array.isArray(authors) && authors) {
            val = [authors];
        }
        const authorsList = val.map((author) => {
            /* eslint-disable camelcase */
            let { first_name, last_name, year_of_birth, year_of_death } = author;
            if (!year_of_birth) {
                year_of_birth = "";
            }
            if (!year_of_death) {
                year_of_death = "";
            }
            if (!first_name) {
                first_name = "";
            }
            if (!last_name) {
                last_name = "";
            }

            let year = "?";
            if (year_of_birth !== "" || year_of_death !== "") {
                year = `${year_of_birth}-${year_of_death}`;
            }

            let name = "Unknown";
            if (first_name !== "" || last_name !== "") {
                name = `${first_name} ${last_name}`;
            }

            return `${name} (${year})`;
        });

        const lastAuthor = authorsList.pop();
        if (authorsList.length === 0) {
            return lastAuthor;
        }

        const firstAuthors = authorsList.join(", ");

        return `${firstAuthors} and ${lastAuthor}`;
    };

    const subjectsToText = (subjects) => subjects?.join(", ");

    const renderResult = (book) => (
        <Container key={book.id} sx={{ marginBottom: "3em" }}>
            <Typography sx={{ fontSize: 34, margin: "0" }} color="text.secondary" gutterBottom>
                <a href={`/book/${book.id}`}>{book.title}</a>
            </Typography>
            <Typography sx={{ fontSize: 18, margin: "0" }} color="text.secondary" gutterBottom>
                Authored by {authorsToText(book.authors)}
            </Typography>
            <Typography sx={{ fontSize: 12, margin: "0" }} color="text.secondary" gutterBottom>
                {subjectsToText(book.subjects)}
            </Typography>
            <Typography sx={{ fontSize: 12, margin: "0" }} color="text.secondary" gutterBottom>
                Released on {dayjs(book.release_date).format("DD MMM YYYY")}
            </Typography>
            <MKButton
                variant="contained"
                color="secondary"
                sx={{ marginTop: "1.5em" }}
                onClick={() => {
                    moreLikeThis(book.id);
                }}
            >
                More Like This
            </MKButton>
            <Box
                sx={{
                    width: 300,
                    display: "flex",
                    alignItems: "center",
                }}
            >
                <Rating
                    value={book.rating}
                    readOnly
                    precision={0.5}
                    emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
                />
                <Typography
                    sx={{ fontSize: 14, margin: "0", marginLeft: "0.2em", lineHeight: "0.1em" }}
                    color="text.secondary"
                    gutterBottom
                >
                    • {book.num_ratings} ratings
                </Typography>
            </Box>
        </Container>
    );

    return (
        <Container sx={{ marginBottom: "3em", marginTop: "3em" }}>
            {!loading && !error && !data.exact_query && data.orig_query !== data.did_you_mean && (
                <Container sx={{ marginBottom: "3em" }}>
                    <Typography
                        sx={{ fontSize: 34, margin: "0" }}
                        color="text.secondary"
                        gutterBottom
                    >
                        Did you mean &quot;{data.did_you_mean}&quot;?
                    </Typography>
                    <Typography
                        sx={{ fontSize: 18, margin: "0" }}
                        color="text.secondary"
                        gutterBottom
                    >
                        Search for &quot;
                        {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
                        <a href="#" onClick={() => props.exactSearch(data)}>
                            {data.orig_query}
                        </a>
                        &quot; instead.
                    </Typography>
                </Container>
            )}
            {loading && (
                <Box sx={{ display: "flex" }}>
                    <CircularProgress sx={{ marginLeft: "auto", marginRight: "auto" }} />
                </Box>
            )}
            {error && (
                <Box sx={{ display: "flex" }}>
                    <Typography
                        sx={{
                            fontSize: 32,
                            lineHeight: "0.1em",
                            marginLeft: "auto",
                            marginRight: "auto",
                        }}
                        color="text.secondary"
                        gutterBottom
                    >
                        {ERROR_MESSAGE}
                    </Typography>
                </Box>
            )}
            {!loading && !error && data.docs.length === 0 && (
                <Box sx={{ display: "flex" }}>
                    <Typography
                        sx={{
                            fontSize: 32,
                            lineHeight: "0.1em",
                            marginLeft: "auto",
                            marginRight: "auto",
                        }}
                        color="text.secondary"
                        gutterBottom
                    >
                        {NO_RESULTS_MESSAGE}
                    </Typography>
                </Box>
            )}
            {!loading && !error && data.docs.map((book) => renderResult(book))}
        </Container>
    );
}

SearchResults.propTypes = {
    loading: PropTypes.bool.isRequired,
    error: PropTypes.bool.isRequired,
    data: PropTypes.object.isRequired /* eslint-disable-line react/forbid-prop-types */,
    moreLikeThis: PropTypes.func.isRequired,
    exactSearch: PropTypes.func.isRequired,
};

export default SearchResults;
