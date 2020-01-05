import {
  AppBar,
  Box,
  Container,
  createMuiTheme,
  CssBaseline,
  ThemeProvider,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { ItemList } from 'app/components/Item';
import React from 'react';

const View: React.FC = () => {
  // const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const prefersDarkMode = true;

  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode],
  );
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box>
        <AppBar position="static" color="default">
          <Toolbar>
            <Typography variant="h6">SScroll</Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="sm">
          <ItemList></ItemList>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default View;
