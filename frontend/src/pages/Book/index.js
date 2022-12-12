// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKTypography from "components/MKTypography";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";
import DefaultFooter from "examples/Footers/DefaultFooter";

// Routes
import routes from "routes";
import footerRoutes from "footer.routes";

// Images
import bgImage from "assets/images/bg-book.jpg";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "api";
import {
    CircularProgress,
    Rating,
    Typography,
    Box,
    ToggleButtonGroup,
    ToggleButton,
} from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import dayjs from "dayjs";
import MKBadge from "components/MKBadge";

function Book() {
    const { id } = useParams();
    const [fetchResults, setFetchResults] = useState({
        loading: true,
        data: {},
        error: false,
    });

    const [infoTab, setInfoTab] = useState("transcription");

    const handleInfoTab = (_event, newValue) => {
        if (newValue !== null) {
            setInfoTab(newValue);
        }
    };

    const ERROR_MESSAGE = "An error occurred  while fetching book :(";

    const fetchBook = async () => {
        try {
            const response = await api.get(`book/${id}`);
            if (response.status === 200) {
                setFetchResults({
                    loading: false,
                    data: response.data,
                    error: false,
                });
            } else {
                setFetchResults({ loading: false, data: {}, error: true });
            }
        } catch (e) {
            setFetchResults({ loading: false, data: {}, error: true });
        }
    };

    useEffect(() => fetchBook(), []);

    const authorsToText = (authors) => {
        let val = authors || [];
        if (!Array.isArray(authors)) {
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

        if (authorsList.length === 0) {
            return "Unknown";
        }

        const lastAuthor = authorsList.pop();
        if (authorsList.length === 0) {
            return lastAuthor;
        }

        const firstAuthors = authorsList.join(", ");

        return `${firstAuthors} and ${lastAuthor}`;
    };

    const subjectsToText = (subjects) => subjects.join(", ");

    const getBestEntity = (nerEntities) => {
        // conver nerEntities to lower case
        const nerEntitiesLower = nerEntities.map((entity) => entity.toLowerCase());
        // get the entity that appears the most
        const bestEntity = nerEntitiesLower.reduce(
            (a, b, i, arr) =>
                arr.filter((v) => v === a).length >= arr.filter((v) => v === b).length ? a : b,
            null
        );
        return bestEntity;
    };

    const bookInfo = (book) => (
        <>
            <MKTypography
                variant="h1"
                color="white"
                sx={({ breakpoints, typography: { size } }) => ({
                    [breakpoints.down("md")]: {
                        fontSize: size["3xl"],
                    },
                })}
            >
                {book.title}
            </MKTypography>
            <MKTypography variant="body1" color="white" opacity={0.8} mt={1} mb={1}>
                Authored by {authorsToText(book.authors)}
            </MKTypography>
            <MKTypography variant="body1" color="white" opacity={0.8} mt={1} mb={3}>
                {subjectsToText(book.subjects)}
            </MKTypography>
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                }}
            >
                {book.rating ? (
                    <Rating
                        value={book.rating}
                        readOnly
                        precision={0.5}
                        emptyIcon={
                            <StarIcon style={{ color: "white", opacity: 0.3 }} fontSize="inherit" />
                        }
                    />
                ) : (
                    ""
                )}
                {book.num_ratings ? (
                    <MKTypography
                        variant="body1"
                        color="white"
                        opacity={0.8}
                        sx={{ fontSize: 14, margin: "0", marginLeft: "0.2em", lineHeight: "0.1em" }}
                    >
                        • {book.num_ratings} ratings
                    </MKTypography>
                ) : (
                    ""
                )}
            </Box>
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                }}
            >
                {book.location_book ? <MKBadge value={getBestEntity(book.location_book)} /> : ""}
                {book.person_book ? <MKBadge value={getBestEntity(book.person_book)} /> : ""}
                {book.date_book ? <MKBadge value={getBestEntity(book.date_book)} /> : ""}
            </Box>
            <MKTypography variant="body1" color="white" opacity={0.8} mt={1} mb={3}>
                Released on {dayjs(book.release_date).format("DD MMM YYYY")}
            </MKTypography>
        </>
    );

    const reviewsInfo = (book) => {
        let val = book.reviews || [];
        if (!Array.isArray(book.reviews) && book.reviews !== undefined) {
            val = [book.reviews];
        }
        return val.map((review) => (
            <Container key={review.id} sx={{ marginBottom: "3em", textAlign: "justify" }}>
                <Typography sx={{ fontSize: 34, margin: "0" }} color="text.secondary" gutterBottom>
                    <b>
                        {review.user_name && review.user_name !== ""
                            ? review.user_name
                            : "Anonymous"}
                    </b>{" "}
                    on {dayjs(review.date).format("DD MMM YYYY")}
                </Typography>
                <Box
                    sx={{
                        marginBottom: "0.5em",
                        display: "flex",
                        alignItems: "center",
                    }}
                >
                    {review.rating && (
                        <Rating
                            value={review.rating}
                            readOnly
                            precision={0.5}
                            emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
                        />
                    )}
                    <Typography
                        sx={{ fontSize: 14, margin: "0", marginLeft: "0.2em", lineHeight: "0.1em" }}
                        color="text.secondary"
                        gutterBottom
                    >
                        {review.rating && "•"} {review.num_likes ? review.num_likes : 0} likes
                    </Typography>
                </Box>

                {review.text &&
                    review.text.split("\n").map((paragraph, index) => (
                        <div
                            style={{ marginBottom: "1.5em" }}
                            key={index /* eslint-disable-line react/no-array-index-key */}
                        >
                            <MKTypography
                                variant="body1"
                                sx={({ breakpoints, typography: { size } }) => ({
                                    [breakpoints.down("md")]: {
                                        fontSize: size["3l"],
                                    },
                                })}
                            >
                                {paragraph}
                            </MKTypography>
                        </div>
                    ))}
            </Container>
        ));
    };

    const textInfo = (book) => (
        <>
            {book.text.split("\n").map((paragraph, index) => (
                <div
                    style={{ marginBottom: "1.5em", textAlign: "justify" }}
                    key={index /* eslint-disable-line react/no-array-index-key */}
                >
                    <MKTypography
                        variant="body1"
                        sx={({ breakpoints, typography: { size } }) => ({
                            [breakpoints.down("md")]: {
                                fontSize: size["3l"],
                            },
                        })}
                    >
                        {paragraph}
                    </MKTypography>
                </div>
            ))}
        </>
    );
    return (
        <>
            <DefaultNavbar routes={routes} />
            <MKBox
                minHeight="75vh"
                width="100%"
                sx={{
                    backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.75)), url(${bgImage})`,
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    display: "grid",
                    placeItems: "center",
                }}
            >
                <Grid
                    container
                    item
                    xs={12}
                    lg={8}
                    justifyContent="center"
                    alignItems="center"
                    flexDirection="column"
                    sx={{ mx: "auto", textAlign: "center" }}
                >
                    {fetchResults.loading && (
                        <Box sx={{ display: "flex" }}>
                            <CircularProgress sx={{ marginLeft: "auto", marginRight: "auto" }} />
                        </Box>
                    )}
                    {fetchResults.error && (
                        <Box sx={{ display: "flex" }}>
                            <MKTypography
                                variant="h1"
                                color="white"
                                sx={({ breakpoints, typography: { size } }) => ({
                                    [breakpoints.down("md")]: {
                                        fontSize: size["3xl"],
                                    },
                                })}
                            >
                                {ERROR_MESSAGE}
                            </MKTypography>
                        </Box>
                    )}
                    {!fetchResults.loading && !fetchResults.error && bookInfo(fetchResults.data)}
                </Grid>
            </MKBox>
            <Card
                sx={{
                    p: 2,
                    mx: { xs: 2, lg: 3 },
                    mt: -8,
                    mb: 4,
                    boxShadow: ({ boxShadows: { xxl } }) => xxl,
                }}
            >
                <Container sx={{ marginBottom: "3em", marginTop: "3em" }}>
                    <Container sx={{ maxWidth: "45em!important" }}>
                        {fetchResults.loading && (
                            <Box sx={{ display: "flex" }}>
                                <CircularProgress
                                    sx={{ marginLeft: "auto", marginRight: "auto" }}
                                />
                            </Box>
                        )}
                        {fetchResults.error && (
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
                        {!fetchResults.loading && !fetchResults.error && (
                            <ToggleButtonGroup
                                color="primary"
                                sx={{ marginBottom: "3em" }}
                                value={infoTab}
                                exclusive
                                onChange={handleInfoTab}
                            >
                                <ToggleButton value="transcription">Transcription</ToggleButton>
                                <ToggleButton value="reviews">Reviews</ToggleButton>
                            </ToggleButtonGroup>
                        )}
                        {!fetchResults.loading &&
                            !fetchResults.error &&
                            infoTab === "transcription" &&
                            textInfo(fetchResults.data)}
                        {!fetchResults.loading &&
                            !fetchResults.error &&
                            infoTab === "reviews" &&
                            reviewsInfo(fetchResults.data)}
                    </Container>
                </Container>
            </Card>
            <MKBox pt={6} px={1} mt={6}>
                <DefaultFooter content={footerRoutes} />
            </MKBox>
        </>
    );
}

export default Book;
