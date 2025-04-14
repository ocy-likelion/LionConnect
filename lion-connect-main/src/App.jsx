import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import styled from "styled-components";
import { theme } from "./styles/theme";
import { ThemeProvider } from "styled-components";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import LandingPage from "./pages/LandingPage";
import StudentSignupPage from "./pages/StudentSignupPage";
import CompanySignupPage from "./pages/CompanySignupPage";
import LoginPage from "./pages/LoginPage";
import CategoryListingPage from "./pages/CategoryListingPage";
import CompanyServicePage from "./pages/CompanyServicePage";
import MyPage from "./pages/MyPage";

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: ${theme.colors.background};
`;

const Nav = styled.nav`
  background-color: white;
  padding: ${theme.spacing.md} ${theme.spacing.xl};
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
`;

const NavContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled(Link)`
  font-size: ${theme.typography.h2.fontSize};
  font-weight: bold;
  color: ${theme.colors.primary};
  text-decoration: none;
`;

const NavLinks = styled.div`
  display: flex;
  gap: ${theme.spacing.lg};
`;

const NavLink = styled(Link)`
  color: ${theme.colors.text};
  text-decoration: none;
  font-size: ${theme.typography.body.fontSize};

  &:hover {
    color: ${theme.colors.primary};
  }
`;

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AppContainer>
          <Nav>
            <NavContainer>
              <Logo to="/">라이언 커넥트</Logo>
              <NavLinks>
                <NavLink to="/login">로그인/회원가입</NavLink>
                <NavLink to="/mypage">마이페이지</NavLink>
                <NavLink to="/company">기업서비스</NavLink>
              </NavLinks>
            </NavContainer>
          </Nav>

          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup/student" element={<StudentSignupPage />} />
            <Route path="/signup/company" element={<CompanySignupPage />} />
            <Route path="/category" element={<CategoryListingPage />} />
            <Route path="/company" element={<CompanyServicePage />} />
            <Route path="/mypage" element={<MyPage />} />
          </Routes>
        </AppContainer>
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </Router>
    </ThemeProvider>
  );
};

export default App;
