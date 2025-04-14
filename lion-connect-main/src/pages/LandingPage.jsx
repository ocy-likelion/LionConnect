import React from "react";
import styled, { keyframes } from "styled-components";
import { useNavigate } from "react-router-dom";
import { theme } from "../styles/theme";
import {
  FaPalette,
  FaMobileAlt,
  FaCode,
  FaServer,
  FaChartLine,
  FaCloud,
  FaBullhorn,
  FaGamepad,
  FaCube,
} from "react-icons/fa";

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${theme.spacing.xl};
  background-color: ${theme.colors.background};
`;

const HeroSection = styled.section`
  text-align: center;
  padding: 6rem 0;
  background: linear-gradient(
    135deg,
    ${theme.colors.primary} 0%,
    ${theme.colors.secondary} 100%
  );
  border-radius: 2rem;
  margin-bottom: 4rem;
  color: white;
  animation: ${fadeIn} 1s ease-out;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: ${theme.spacing.lg};
  background: linear-gradient(45deg, #fff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: ${theme.spacing.xl};
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  justify-content: center;
  margin-bottom: ${theme.spacing.xl};
`;

const Button = styled.button`
  background-color: white;
  color: ${theme.colors.primary};
  padding: 1rem 2rem;
  border-radius: 2rem;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
`;

const CategorySection = styled.section`
  margin-top: ${theme.spacing.xl};
  padding: 4rem 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.9),
    rgba(255, 255, 255, 0.7)
  );
`;

const CategoryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: ${theme.spacing.lg};
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const CategoryCard = styled.div`
  background-color: white;
  padding: 2.5rem 2rem;
  border-radius: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(
      90deg,
      ${theme.colors.primary},
      ${theme.colors.secondary}
    );
  }

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  }
`;

const CategoryIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: ${theme.colors.primary};
  transition: transform 0.3s ease;

  ${CategoryCard}:hover & {
    transform: scale(1.1);
  }
`;

const CategoryName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.colors.text};
  margin-bottom: 0.5rem;
`;

const CategoryDescription = styled.p`
  font-size: 0.9rem;
  color: ${theme.colors.gray};
  margin: 0;
`;

const SectionTitle = styled.h2`
  font-size: 2.5rem;
  color: ${theme.colors.text};
  margin-bottom: 3rem;
  text-align: center;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 4px;
    background: linear-gradient(
      90deg,
      ${theme.colors.primary},
      ${theme.colors.secondary}
    );
    border-radius: 2px;
  }
`;

const categories = [
  {
    name: "UI/UX",
    icon: <FaPalette />,
    description: "사용자 경험과 인터페이스 디자인",
  },
  {
    name: "앱개발",
    icon: <FaMobileAlt />,
    description: "모바일 애플리케이션 개발",
  },
  {
    name: "프론트엔드",
    icon: <FaCode />,
    description: "웹 프론트엔드 개발",
  },
  {
    name: "백엔드",
    icon: <FaServer />,
    description: "서버 및 백엔드 개발",
  },
  {
    name: "데이터분석",
    icon: <FaChartLine />,
    description: "데이터 분석 및 시각화",
  },
  {
    name: "클라우드 엔지니어링",
    icon: <FaCloud />,
    description: "클라우드 인프라 구축 및 운영",
  },
  {
    name: "그로스 마케터",
    icon: <FaBullhorn />,
    description: "데이터 기반 성장 전략 수립",
  },
  {
    name: "유니티 게임 개발",
    icon: <FaGamepad />,
    description: "Unity 엔진 기반 게임 개발",
  },
  {
    name: "블록체인",
    icon: <FaCube />,
    description: "블록체인 기술 개발 및 적용",
  },
];

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <HeroSection>
        <Title>라이언 커넥트</Title>
        <Subtitle>KDT 수료생들과 기업을 연결하는 채용 플랫폼</Subtitle>
        <ButtonGroup>
          <Button onClick={() => navigate("/signup/student")}>
            수료생으로 시작하기
          </Button>
          <Button onClick={() => navigate("/signup/company")}>
            기업으로 시작하기
          </Button>
        </ButtonGroup>
      </HeroSection>

      <CategorySection>
        <SectionTitle>카테고리별 인재 찾기</SectionTitle>
        <CategoryGrid>
          {categories.map((category) => (
            <CategoryCard key={category.name}>
              <CategoryIcon>{category.icon}</CategoryIcon>
              <CategoryName>{category.name}</CategoryName>
              <CategoryDescription>{category.description}</CategoryDescription>
            </CategoryCard>
          ))}
        </CategoryGrid>
      </CategorySection>
    </Container>
  );
};

export default LandingPage;
