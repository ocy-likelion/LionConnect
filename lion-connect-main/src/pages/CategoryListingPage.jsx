import React, { useState } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${theme.spacing.xl};
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${theme.spacing.xl};
`;

const Title = styled.h1`
  font-size: ${theme.typography.h1.fontSize};
  color: ${theme.colors.text};
`;

const FilterSection = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.xl};
`;

const FilterButton = styled.button`
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.md};
  background-color: ${(props) =>
    props.active ? theme.colors.primary : "white"};
  color: ${(props) => (props.active ? "white" : theme.colors.text)};
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background-color: ${(props) =>
      props.active ? theme.colors.secondary : theme.colors.lightGray};
  }
`;

const StudentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: ${theme.spacing.lg};
`;

const StudentCard = styled.div`
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.md};
  padding: ${theme.spacing.lg};
  background-color: white;
`;

const StudentName = styled.h3`
  font-size: ${theme.typography.h2.fontSize};
  margin-bottom: ${theme.spacing.sm};
`;

const StudentInfo = styled.p`
  color: ${theme.colors.gray};
  margin-bottom: ${theme.spacing.sm};
`;

const Skills = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: ${theme.spacing.xs};
  margin-bottom: ${theme.spacing.md};
`;

const SkillTag = styled.span`
  background-color: ${theme.colors.lightGray};
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.sm};
  font-size: ${theme.typography.body.fontSize};
`;

const PortfolioLink = styled.a`
  color: ${theme.colors.primary};
  text-decoration: none;
  display: block;
  margin-top: ${theme.spacing.md};

  &:hover {
    text-decoration: underline;
  }
`;

const CategoryListingPage = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedFilter, setSelectedFilter] = useState("recent");

  const categories = [
    "all",
    "UI/UX",
    "앱개발",
    "프론트엔드",
    "백엔드",
    "데이터분석",
  ];

  const filters = ["recent", "popular", "recommended"];

  // 임시 데이터
  const students = [
    {
      id: 1,
      name: "김수료",
      course: "KDT 프론트엔드",
      skills: ["React", "JavaScript", "HTML", "CSS"],
      portfolio: "https://example.com/portfolio",
    },
    // 더 많은 학생 데이터 추가 가능
  ];

  return (
    <Container>
      <Header>
        <Title>인재 찾기</Title>
      </Header>

      <FilterSection>
        {categories.map((category) => (
          <FilterButton
            key={category}
            active={selectedCategory === category}
            onClick={() => setSelectedCategory(category)}
          >
            {category === "all" ? "전체" : category}
          </FilterButton>
        ))}
      </FilterSection>

      <FilterSection>
        {filters.map((filter) => (
          <FilterButton
            key={filter}
            active={selectedFilter === filter}
            onClick={() => setSelectedFilter(filter)}
          >
            {filter === "recent"
              ? "최신순"
              : filter === "popular"
              ? "인기순"
              : "추천순"}
          </FilterButton>
        ))}
      </FilterSection>

      <StudentGrid>
        {students.map((student) => (
          <StudentCard key={student.id}>
            <StudentName>{student.name}</StudentName>
            <StudentInfo>{student.course}</StudentInfo>
            <Skills>
              {student.skills.map((skill) => (
                <SkillTag key={skill}>{skill}</SkillTag>
              ))}
            </Skills>
            <PortfolioLink
              href={student.portfolio}
              target="_blank"
              rel="noopener noreferrer"
            >
              포트폴리오 보기
            </PortfolioLink>
          </StudentCard>
        ))}
      </StudentGrid>
    </Container>
  );
};

export default CategoryListingPage;
